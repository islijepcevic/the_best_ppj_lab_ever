'''akcija tablice akcija'''

from analizator.zajednicki.produkcija import Produkcija

class Akcija:
    
    def __init__( self, tip, vrijednost = None ):
        '''string tip - 'pomakni' ili 'reduciraj' ili 'prihvati' ili 'odbaci'
        
        ako je tip 'pomakni' - ocekuje se int
        ako je tip 'reduciraj' - ocekuje se objekt Produkcije
        '''
        
        self.tip_akcije = self.vrijednost = None
        
        tocan_input = False
        
        if tip == 'pomakni':
            self.tip = tip
            
            if type( vrijednost ) == int:
                self.vrijednost = vrijednost
                tocan_input = True
        
        elif tip == 'reduciraj':
            self.tip = tip
            
            if type( vrijednost ) == Produkcija:
                self.vrijednost = vrijednost
                tocan_input = True
        
        elif tip == 'prihvati':
            self.tip = tip
            
        elif tip == 'odbaci':
            self.tip = tip
        
        if not tocan_input:
            raise TypeError( 'pokusaj stvaranja krivog tipa akcije' )
        
        # ako je sve dobro na kraju postoje:
            # self.tip          - 'pomakni' ili 'reduciraj'
            # self.vrijednost   - int ili instanca Produkcije
    
    
    def __repr__( self ):
        '''metoda koja omogucava da se pri pozivu funkcije repr nad objektom ove
        klase pravilno izvrsi pretvorba u string, tako da kad se pozove eval,
        da se pravilno mogu ucitati sve vrijednosti
        
        IVAN
        '''
        return 'Akcija("' + self.tip + '","' + repr( self.vrijednost ) + '")'
