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
        pass
    
    
    def _epsilon_okruzenje( self ):
        '''postoji kod za ovo u prvom labosu, u analizatoru; mozda treba
        prilagoditi tipove i neke detalje, nisam gledao
        
        MAK
        '''
        pass
    
    
    def prijelaz_za_niz( self, niz ):
        '''delta s kapicom, kako je to bilo oznacavano u utr-u
        trebalo bi samo prosirit se po epsilon okruzenju kolko se sjecam
        
        MAK
        '''
        pass
