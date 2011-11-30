'''akcija tablice akcija'''

class Akcija:
    
    def __init__( self, tip, vrijednost ):
        '''string tip - 'pomakni' ili 'reduciraj'
        
        ako je tip 'pomakni' - ocekuje se int
        ako je tip 'reduciraj' - ocekuje se objekt Produkcije
        '''
        
        self.tip_akcije = self.akcija = None
        
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
        
        if not tocan_input:
            raise TypeError
