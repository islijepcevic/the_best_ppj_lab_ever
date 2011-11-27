'''gramatika'''

from generator.produkcija import Produkcija

class Gramatika:
    
    def __init__( self, nezavrsni_znakovi, zavrsni_znakovi, pocetni_nezavrsni,
                produkcije ):
        
        # tipovi definirani u parseru
        self.nezavrsni_znakovi = nezavrsni_znakovi  # skup stringova
        self.zavrsni_znakovi = zavrsni_znakovi      # skup stringova
        self.pocetni_nezavrsni = pocetni_nezavrsni  # string
        self.produkcije = self.produkcije           # niz instanci Produkcije
        
        self.prazni_nezavrsni_znakovi = set([])
        self._zapocinje_znakom = {}  # matrica, bit ce dict unutar dicta, svaki
                                    # sa jednakim kljucevima. sadrzavat ce prvo
                                    # ZapocinjeIzravnoZnakom, pa onda
                                    # ZapocinjeZnakom, str 101 - 102
        self._zapocinje = {}     # kljuc je JEDAN nezavrsni znak, vrijednost je
                                # skup zavrsnih znakova, str 102, prvi algoritam
        
        # ovo se slijedom dogadja kako bi se gramatika pripremila da daje
        # skup zapocni( niz_znakova )
        self._dodaj_novi_pocetni_nezavrsni()
        self._odredi_prazne_znakove()
        self._odredi_zapocinje_izravno_znakom()
        self._odredi_zapocinje_znakom()
        self._odredi_zapocinje_za_nezavrsne()
        
        
    def _dodaj_novi_pocetni_nezavrsni( self ):
        '''Funkcija koja mora dodati novi pocetni nezavrsni znak. Dodaje ga u 
        skup nezavrsnih, u pocetni_nezavrsni te dodaje novu inicijalnu
        produkciju na pocetak niza produkcije.
        
        PETAR
        '''
        
        '''napomena: napravi tako da ime novog nezavrsnog znaka bude:
        "<<novi_nezavrsni_znak>>"
        takvo ime se sigurno nece pojaviti u ulaznoj datoteci
        '''
        pass
    
    
    def _odredi_prazne_znakove( self ):
        '''
        PETAR
        '''
        pass
    
    
    def _odredi_zapocinje_izravno_znakom( self ):
        '''
        PETAR
        '''
        pass
    
    
    def _odredi_zapocinje_znakom( self ):
        '''
        IVAN
        '''
        pass
    
    
    def _odredi_zapocinje_za_nezavrsne( self ):
        '''
        PETAR
        '''
        pass
    
    
    def odredi_zapocinje_za_niz( self, niz ):
        '''str 102 - 103
        PETAR
        '''
        pass
