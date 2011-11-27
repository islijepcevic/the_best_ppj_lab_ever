'''ovo je parser'''

from generator.gramatika import Gramatika
from generator.produkcija import Produkcija

class Parser:
    
    def __init__( self, ulazni_tok ):
        '''konstruktor'''
        
        # ulazna datoteka - niz (ili lista) stringova kakvi su zadani u zadatku
        # vec odvojeni po znaku za novi redak
        self.ulazna_datoteka = ulazni_tok.read().split('\n')
        
        # podaci gramatike
        self.nezavrsn_znakovi = set([])     # skup stringova
        self.zavrsni_znakovi = set([])      # skup stringova
        self.pocetni_nezavrsni_znak = ''    # string
        self.produkcije = []                # niz objekata produkcija, mora biti
                                            # niz jer je bitan poredak
        
        # sinkronizacijski znakovi
        self.sinkronizacijski_znakovi = set([]) # skup stringova
    
    
    def ucitaj_gramatiku( self ):
        '''iz ulazne datoteke ucitava podatke i stvara (te vraca) instancu
        Gramatike
        
        ZORAN
        '''
        
        '''
        Zorane, ovdje prolazis vec pripremljeni niz self.ulazna_datoteka i 
        popunjavas ostale podatke. Ako nesto nije jasno, javi se cim prije!
        
        Pazi kako stvaras produkcije! Treba za svaku stvoriti novi objekt klase
        Produkcija. Klasa Produkcija je zapravo samo struktura, jer nema nikakve
        metode, nego sluzi samo da sadrzi podatke o produkciji.
        '''
        
        return Gramatika( self.nezavrsni_znakovi, self.zavrsni_znakovi,
                        self.pocetni_nezavrsni_znak, self.produkcije )
    
    
    def ispisi_sinkronizacijske_znakove( self ):
        '''ispisuje sinkronizacijske znakove u neku datoteku za sintaksni
        analizator. oni nisu potrebni generatoru pa ih ovaj parser niti ne salje
        generatoru niti ih ne stavlja u gramatiku
        
        IVAN
        '''
        pass
