'''epsilon nka model'''

from generator.nka import NKA
from generator.dka import DKA
from generator.prijelazi import Prijelazi
from analizator.zajednicki.stog import Stog

class ENKA:
    
    def __init__( self, stanja, ulazni_znakovi, prijelazi ):
        
        '''
        # OLD VERSION
        self.stanja                 = set(stanja)           # skup LR1Stavki
        self.prihvatljiva           = set(prihvatljiva)     # skup LR1Stavki
        self.ulazni_znakovi         = set(ulazni_znakovi)   # skup stringova
        self.pocetno_stanje         = pocetno_stanje        # LR1Stavka
        self.prijelazi              = prijelazi             # rjecnik: kljuc = par (LR1Stavka, string)
                                                            # vrijednost = skup LR1Stavki
        '''
        
        self.stanja = stanja        # niz LRStavki - sva prihvatljiva; prvo pocetno
        self.prijelazi = prijelazi  # objekt Prijelazi
        self.abeceda = ulazni_znakovi   # set stringova
        
        self._pocetno_stanje_index = 0
        
        # ovdje se pamte izracunata epsilon okruzenja
        # kad jedno okruzenje bude izracunato, vrijednost ovog niza na indexu
        # zeljenog stanja postaje skup indexa na sva stanja e-okruzenja
        self._eokruzenja = [None] * len( self.stanja )
        
        
        print( len(self.stanja), len(self.abeceda) )
        '''napomena: u knjizi pise da su sva stanja prihvatljiva, treba jos
        prokuziti da li da se doda dodatno neprihvatljivo stanje i kad/gdje'''
    
    
    def kreiraj_dka( self ):
        '''stvaranje dka direktno iz enkas'''
        
        # treba vratiti frozenset indexa stanja/stavki
        dka_pocetno = self._epsilon_okruzenje( self._pocetno_stanje_index )
        
        stanja_dka = [ dka_pocetno  ]
        
        postoji_neprihvatljivo = False
        
        neobradjena = Stog( 0 )
        
        prijelazi_dka = Prijelazi() # dict( int_stanje: dict( znak: int_stanje ) )
        
        # varijable samo za test ispis
        i = 0
        nz = len( self.abeceda ) + 1
        
        while not neobradjena.jest_prazan():
            # test ispisi
            print()
            print( i, neobradjena.duljina )
            i += 1
            
            index_stanja_za_obradu = neobradjena.dohvati_vrh()
            neobradjena.skini()
            
            stanje_za_obradu = stanja_dka[ index_stanja_za_obradu ]
            
            j=0
            for z in (self.abeceda | set(['<<!>>'])):
                
                novo_stanje = set() # postaje set intova (indexa stavki)
                
                # test ispisi
                print( j, '/', nz, len(stanje_za_obradu) )
                j+=1
                
                for index_stavke in stanje_za_obradu:
                    novo_stanje.update( self.prijelaz_za_niz( index_stavke, [z] ) )
                
                novo_stanje = frozenset( novo_stanje )
                
                if novo_stanje:
                    
                    try:
                        index_novog = stanja_dka.index( novo_stanje )
                    
                    except:
                        index_novog = len( stanja_dka )
                        neobradjena.stavi( index_novog )
                        stanja_dka.append( novo_stanje )
                    
                    prijelazi_dka.dodaj( index_stanja_za_obradu, z, index_novog )
                
                else:
                    postoji_neprihvatljivo = True
                    prijelazi_dka.dodaj( index_stanja_za_obradu, z, -1 )
        
        print( 'stvaram dka')
        
        return DKA( self.stanja, stanja_dka, self.abeceda, prijelazi_dka )
    
    
    def _epsilon_okruzenje( self, index_stanja ):
        '''postoji kod za ovo u prvom labosu, u analizatoru; mozda treba
        prilagoditi tipove i neke detalje, nisam gledao
        
        dodatno: vraca se skup indexa na stavke
        
        MAK
        '''
        
        if self._eokruzenja[ index_stanja ] is not None:
            return self._eokruzenja[ index_stanja ]
        
        #stanje = self.stanja[ index_stanja ]
        
        #trSt = {stanje} # set
        trSt = { index_stanja }
        
        #S = [stanje]    #stog
        S = Stog( index_stanja )
        
        #while len(S) != 0:
        while not S.jest_prazan():
            
            #t = S.pop()                             #jedno stanje
            t_index = S.dohvati_vrh()
            S.skini()
            
            L = self.prijelazi.dohvati( t_index, '$' )
            #L = self.prijelazi.get( (t, '$'), set() )  # skup stanja
            
            for v_index in L:
                if v_index not in trSt:
                    trSt.add(v_index)
                    #S.append(v)
                    S.stavi( v_index )
        
        trSt = frozenset( trSt )
        
        self._eokruzenja[ index_stanja ] = trSt
        
        return trSt
    
    
    def _eps_okruzenje_set (self, stanja_indexi):
        novaStanja = set()
        for stanje_index in stanja_indexi:
            novaStanja = novaStanja.union (self._epsilon_okruzenje(stanje_index))
        
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
    
    
    def prijelaz_za_niz( self, index_stanja, niz ):
        '''delta s kapicom, kako je to bilo oznacavano u utr-u
        trebalo bi samo prosirit se po epsilon okruzenju kolko se sjecam
        
        MAK
        '''
        # AKO NE BUDE RADILO: ALGORITAM EKVIVALENTAN UDZBENIKU UTR:
        # IVAN
        
        if not niz:
            return self._epsilon_okruzenje( index_stanja )
        
        znak = niz[-1]
        
        eP = self.prijelaz_za_niz( index_stanja, niz[:-1] )   # za niz duljine 1, niz[:1]==[]
        
        P = set()
        
        for estanje_index in eP:
            P.update( self.prijelazi.dohvati( estanje_index, znak ) )
        
        return self._eps_okruzenje_set( P )
