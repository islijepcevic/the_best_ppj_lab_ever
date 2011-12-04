'''epsilon nka model'''

from generator.nka import NKA

class ENKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        
        self.stanja                 = set(stanja)           # skup LR1Stavki
        self.prihvatljiva           = set(prihvatljiva)     # skup LR1Stavki
        self.ulazni_znakovi         = set(ulazni_znakovi)   # skup stringova
        self.pocetno_stanje         = pocetno_stanje        # LR1Stavka
        self.prijelazi              = prijelazi             # rjecnik: kljuc = par (LR1Stavka, string)
                                                            # vrijednost = skup LR1Stavki
        
        '''napomena: u knjizi pise da su sva stanja prihvatljiva, treba jos
        prokuziti da li da se doda dodatno neprihvatljivo stanje i kad/gdje'''
    
    
    def kreiraj_nka( self ):
        '''vraca instancu NKA
        MAK
        '''

        prijelaziNka = dict()
        for stanje in self.stanja:
            for znak in self.ulazni_znakovi:
                klj = (stanje, znak)

                novaStanja = self._epsilon_okruzenje(stanje)
                novaStanja = self._prijelaz_za_skup(novaStanja, znak)
                
                if novaStanja:
                    prijelaziNka[klj] = novaStanja.union(self._eps_okruzenje_set(novaStanja))
                
                # AKO NE BUDE RADILO
                '''
                prijelaziNka[klj] |= self.prijelaz_za_niz( stanje, znak )
                '''
    
        
        if self._pocetni_prosiriv_do_prihvatljivih():
            prihvatljivaNka = self.prihvatljiva.union(self.pocetno_stanje)
        else:
            prihvatljivaNka = self.prihvatljiva.copy()
            
        nka = NKA (self.stanja, self.ulazni_znakovi, self.pocetno_stanje,
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
        S = [stanje]
        
        while len(S) != 0:
            t = S.pop()
            L = self.prijelazi.get( (t, '$'), [] )
            for v in (L):
                if v not in trSt:
                    trSt.add(v)
                    S.append(v)
        
        return trSt
    
    def _eps_okruzenje_set (self, stanja):
        novaStanja = set()
        for stanje in stanja:
            novaStanja = novaStanja.union (self._epsilon_okruzenje(stanje))
        
        return novaStanja
    
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
        
        return novaStanja
    
    def prijelaz_za_niz( self, stanje, niz ):
        '''delta s kapicom, kako je to bilo oznacavano u utr-u
        trebalo bi samo prosirit se po epsilon okruzenju kolko se sjecam
        
        MAK
        '''
        
        stanja = self._epsilon_okruzenje(stanje)
        
        #stanjaN = set ()
        
        '''
        for st in stanja:
            for znak in niz:
                stanjaN = stanjaN.union (self._prijelaz(st, znak))
        '''
        
        for znak in niz:
            stanja = self._prijelaz_za_skup( stanja, znak )
        
        '''
        if stanjaN == []:
            return stanja
        
        return stanjaN
        '''
        return stanja
        
        # AKO NE BUDE RADILO: ALGORITAM EKVIVALENTAN UDZBENIKU UTR:
        '''
        P = set()
        for r in self.prijelaz_za_niz( stanje, niz[:-1] ):
            for p in self.prijelazi.get( (r, niz[-1]), set() ):
                P |= p
        return self._eps_okruzenje_set( P )
        '''
