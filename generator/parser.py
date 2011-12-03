'''ovo je parser'''

from generator.gramatika import Gramatika
from analizator.zajednicki.produkcija import Produkcija

class Parser:
    
    def __init__( self, ulazni_tok ):
        '''konstruktor'''
        
        # ulazna datoteka - niz (ili lista) stringova kakvi su zadani u zadatku
        # vec odvojeni po znaku za novi redak
        self.ulazna_datoteka = ulazni_tok.read().split('\n')
        
        # podaci gramatike
        self.nezavrsni_znakovi = set([]) # skup stringova
        self.zavrsni_znakovi = set([]) # skup stringova
        self.pocetni_nezavrsni_znak = '' # string
        self.produkcije = [] # niz objekata produkcija, mora biti
                                            # niz jer je bitan poredak
        
        # sinkronizacijski znakovi
        self.sinkronizacijski_znakovi = set([]) # skup stringova
    
    
    def ucitaj_gramatiku( self ):

        
        self.nezavrsni_znakovi = self.ulazna_datoteka[0].split(' ')
        del self.nezavrsni_znakovi[0]
        self.pocetni_nezavrsni_znak = self.nezavrsni_znakovi[0]
        self.zavrsni_znakovi = self.ulazna_datoteka[1].split(' ')
        del self.zavrsni_znakovi[0]
        self.sinkronizacijski_znakovi = self.ulazna_datoteka[2].split(' ')
        del self.sinkronizacijski_znakovi[0]
        
        
        for i in range(3, len(self.ulazna_datoteka)):
            
            if self.ulazna_datoteka[i].startswith('<'):
                for j in range (i + 1, len(self.ulazna_datoteka)):
                    
                    if self.ulazna_datoteka[j].startswith(' '):
                        self.produkcije.append(Produkcija(self.ulazna_datoteka[i],
                            self.ulazna_datoteka[j].lstrip().split(' ')))

                    else:break
                    
        
        return Gramatika( self.nezavrsni_znakovi, self.zavrsni_znakovi,
                       self.pocetni_nezavrsni_znak, self.produkcije )
    
    
    def ispisi_sinkronizacijske_znakove( self, datoteka ):
        '''ispisuje sinkronizacijske znakove u neku datoteku za sintaksni
        analizator. oni nisu potrebni generatoru pa ih ovaj parser niti ne salje
        generatoru niti ih ne stavlja u gramatiku
        IVAN
        '''
        pass
