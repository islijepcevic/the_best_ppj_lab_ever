'''epsilon nka model'''

from generator.nka import NKA
from analizator.zajednicki.stog import Stog

class ENKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        '''
        # OLD VERSION
        self.stanja                 = set(stanja)           # skup LR1Stavki
        self.prihvatljiva           = set(prihvatljiva)     # skup LR1Stavki
        self.ulazni_znakovi         = set(ulazni_znakovi)   # skup stringova
        self.pocetno_stanje         = pocetno_stanje        # LR1Stavka
        self.prijelazi              = prijelazi             # rjecnik: kljuc = par (LR1Stavka, string)
                                                            # vrijednost = skup LR1Stavki
        '''
        
        self.stanja = stanja        # niz LRStavki - sva prihvatljiva
        self.prijelazi = prijelazi  # niz dictova; key=znak s ulaza; value=set indexa stanja
        self.abeceda = ulazni_znakovi   # set stringova
        
        # ovdje se pamte izracunata epsilon okruzenja
        # kad jedno okruzenje bude izracunato, vrijednost ovog niza na indexu
        # zeljenog stanja postaje skup indexa na sva stanja e-okruzenja
        self._eokruzenja = [None] * len( self.stanja )
        
        
        print( len(self.stanja), len(self.abeceda) )
        '''napomena: u knjizi pise da su sva stanja prihvatljiva, treba jos
        prokuziti da li da se doda dodatno neprihvatljivo stanje i kad/gdje'''
    
    
    def kreiraj_nka( self ):
        '''vraca instancu NKA
        MAK
        '''
        from datetime import datetime
        t1 = datetime.now()
        prijelaziNka = dict()
        z = 0
        for stanje in self.stanja:
            if z % 101 == 0:
                print( z, datetime.now() - t1 )
            z += 1
            for znak in self.ulazni_znakovi:
                klj = (stanje, znak)
                
                # MAK
                '''
                novaStanja = self._epsilon_okruzenje(stanje)
                novaStanja = self._prijelaz_za_skup(novaStanja, znak)
                
                if novaStanja:
                    prijelaziNka[klj] = novaStanja.union(self._eps_okruzenje_set(novaStanja))
                '''
                
                # IVAN
                if klj not in prijelaziNka:
                    prijelaziNka[klj] = self.prijelaz_za_niz( stanje, [znak] )
                else:
                    prijelaziNka[klj] |= self.prijelaz_za_niz( stanje, [znak] )
        
        
        if self._pocetni_prosiriv_do_prihvatljivih():
            prihvatljivaNka = self.prihvatljiva.union({ self.pocetno_stanje })
        else:
            prihvatljivaNka = self.prihvatljiva.copy()
        
        nka = NKA (self.stanja, self.ulazni_znakovi,
                    self._epsilon_okruzenje( self.pocetno_stanje ),
                   prihvatljivaNka, prijelaziNka)
        
        return nka
        
        '''napomena: imam pseudo; u knjizi utr-a str 37'''
        #pass
    
    
    def _pocetni_prosiriv_do_prihvatljivih( self ):
        '''vraca boolan
        vrati true ako je prihvatljivo stanje u epsilon okruzenju pocetnog
        treba za kreiranje NKA
        
        MAK
        '''
        for epsPoc in self._epsilon_okruzenje(self.pocetno_stanje):
            if epsPoc in self.prihvatljiva:
                return True
        
        return False
    
    
    def _epsilon_okruzenje( self, stanje ):
        '''postoji kod za ovo u prvom labosu, u analizatoru; mozda treba
        prilagoditi tipove i neke detalje, nisam gledao
        
        MAK
        '''
        
        trSt = {stanje}
        #S = [stanje]    #stog
        S = Stog( stanje )
        
        hehe = True
        #while len(S) != 0:
        while not S.jest_prazan():
            
            #t = S.pop()                             #jedno stanje
            t = S.dohvati_vrh()
            S.skini()
            L = self.prijelazi.get( (t, '$'), set() )  # skup stanja
            
            
            '''
            bla = len(trSt)
            print(bla)
            
            if bla == 407 :
                print( 407 )
                print( L )
                print()
            
            if bla == 408:
                print( 408 )
                print( L )
                hehe = True
                print()
            
            if bla == 1 and hehe:
                print( 1 )
                print( trSt )
                print()
                #raise BaseException
            '''
            for v in L:
                if v not in trSt:
                    trSt.add(v)
                    #S.append(v)
                    S.stavi( v )
        
        return frozenset( trSt )
    
    def _eps_okruzenje_set (self, stanja):
        novaStanja = set()
        for stanje in stanja:
            novaStanja = novaStanja.union (self._epsilon_okruzenje(stanje))
        
        return frozenset( novaStanja )
    
    def _prijelaz (self, stanje, znak):
        stanja = self.prijelazi.get ((stanje, znak), set())
        
        stanjaN = set()
        if len( stanja ) != 0:
            for st in stanja:
                stanjaN.add (st)
                stanjaN = stanjaN.union(self._epsilon_okruzenje(st))
        
        # vraca prazni set ako na su na pocetku stanja duljine 0
        return stanjaN
    
    def _prijelaz_za_skup (self, stanja, znak):
        novaStanja = set ()
        for s in stanja:
            novaStanja = novaStanja.union(self._prijelaz(s, znak))
        
        return frozenset( novaStanja )
    
    def prijelaz_za_niz( self, stanje, niz ):
        '''delta s kapicom, kako je to bilo oznacavano u utr-u
        trebalo bi samo prosirit se po epsilon okruzenju kolko se sjecam
        
        MAK
        '''
        """
        #stanja = self._epsilon_okruzenje(stanje)
        
        #stanjaN = set ()
        
        '''
        for st in stanja:
            for znak in niz:
                stanjaN = stanjaN.union (self._prijelaz(st, znak))
        '''
        
        #for znak in niz:
            #stanja = self._prijelaz_za_skup( stanja, znak )
        
        '''
        if stanjaN == []:
            return stanja
        
        return stanjaN
        '''
        #return frozenset( stanja )
        """
        # AKO NE BUDE RADILO: ALGORITAM EKVIVALENTAN UDZBENIKU UTR:
        # IVAN
        
        if not niz:
            return frozenset( self._epsilon_okruzenje( stanje ) )
        
        znak = niz[-1]
        
        eP = self.prijelaz_za_niz( stanje, niz[:-1] )   # za niz duljine 1, niz[:1]==[]
        
        P = set()
        
        for estanje in eP:
            P |= self.prijelazi.get( (estanje, znak), set() )
        
        return self._eps_okruzenje_set( P )
