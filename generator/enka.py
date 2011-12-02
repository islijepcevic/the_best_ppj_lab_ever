'''epsilon nka model'''

from generator.nka import NKA

class ENKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        
        self.stanja = stanja                    # skup LR1Stavki
        self.prihvatljiva = prihvatljiva        # skup LR1Stavki
        self.ulazni_znakovi = ulazni_znakovi    # skup stringova
        self.pocetno_stanje = pocetno_stanje    # LR1Stavka
        self.prijelazi = prijelazi      # rjecnik: kljuc = par (LR1Stavka, string)
                                                # vrijednost = skup LR1Stavki
        
        '''napomena: u knjizi pise da su sva stanja prihvatljiva, treba jos
        prokuziti da li da se doda dodatno neprihvatljivo stanje i kad/gdje'''
    
    
    def kreiraj_nka( self ):
        '''vraca instancu NKA
        MAK
        '''
        
        '''napomena: imam pseudo; u knjizi utr-a str 37'''
        pass
    
    
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
     
        trSt = set()
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
        stanja = self.prijelazi.get ((stanje, znak), [])
        
        stanjaN = set()
        if stanja == []:
            return {}
        else:
            for st in stanja:
                stanjaN.add (st)
                stanjaN = stanjaN.union(self._epsilon_okruzenje(st))
                 
        return stanjaN
    
    
    def prijelaz_za_niz( self, stanje, niz ):
        '''delta s kapicom, kako je to bilo oznacavano u utr-u
        trebalo bi samo prosirit se po epsilon okruzenju kolko se sjecam
        
        MAK
        '''
        
        stanja = self._epsilon_okruzenje(stanje)
        
        stanjaN = set ()
        print ("Stanja: " + str(stanja) + "\n")
        for st in stanja:
            for znak in niz:
                print ("st: " + str(st) + "; znak: " + znak + "\n")
                stanjaN = stanjaN.union (self._prijelaz(st, znak))
                print ("stanjaN: " + str(stanjaN) + "\n")
        
        if stanjaN == []:
            return stanja
        
        return stanjaN
            
