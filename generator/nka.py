'''nka model'''

from generator.dka import DKA

class NKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        
        self.stanja = stanja                    # skup LR1Stavki
        self.prihvatljiva = prihvatljiva        # skup LR1Stavki
        self.ulazni_znakovi = ulazni_znakovi    # skup stringova
        self.pocetno_stanje = pocetno_stanje    # LR1Stavka
        self.prijelazi = prijelazi      # rjecnik: kljuc = par (LR1Stavka, string)
                                                # vrijednost = skup LR1Stavki
    
    
    def kreiraj_dka( self ):
        '''vraca instancu DKA
        ovaj algoritam ostavi za kraj, mislim da ga treba malo ubrzati
        generalno: knjiga utr, str 32
        MAK
        '''
        pass
