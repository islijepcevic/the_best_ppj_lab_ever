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
        self.nezavrsni_znakovi = set([])     # skup stringova
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
        
        '''
        Evo malo da nesto napravim, reci ako negdje grijesim pa cu prepravit
        Vjerojatno cu fulat negdje s pretvorbom lista -> set pa me cimni :)
        '''
        
        self.nezavrsni_znakovi = self.ulazna_datoteka[0].split(' ')
        del self.nezavrsni_znakovi[0]
        self.pocetni_nezavrsni_znak = self.nezavrsni_znakovi[0]
        self.zavrsni_znakovi = self.ulazna_datoteka[1].split(' ')
        del self.zavrsni_znakovi[0]
        self.sinkronizacijski_znakovi = self.ulazna_datoteka[2].split(' ')
        del self.sinkronizacijski_znakovi[0]
        
        j=0
        for i in range(len(self.ulazna_datoteka)):
            if i>2:
                if self.ulazna_datoteka[i,0] == '<':
                    self.trenutni_nezavrsni = self.ulazna_datoteka[i]
                else:
                    self.produkcije[j] = Produkcija(self.trenutni_nezavrsni, self.ulazna_datoteka[i])
                    j++
                    
        
        return Gramatika( self.nezavrsni_znakovi, self.zavrsni_znakovi,
                        self.pocetni_nezavrsni_znak, self.produkcije )
    
    
    def ispisi_sinkronizacijske_znakove( self ):
        '''ispisuje sinkronizacijske znakove u neku datoteku za sintaksni
        analizator. oni nisu potrebni generatoru pa ih ovaj parser niti ne salje
        generatoru niti ih ne stavlja u gramatiku
        
        IVAN
        '''
        pass
