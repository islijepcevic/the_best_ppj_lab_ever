'''stog'''

class Stog:
    
    def __init__( self, pocetno_stanje = None ):
        
        self.stog = []
        
        if pocetno_stanje is not None:
            self.stavi( pocetno_stanje )
    
    
    def stavi( self, element ):
        pass
    
    
    def dohvati_vrh( self ):
        '''dohvaca prvih n znakova sa stoga
        '''
        pass
    
    
    def skini( self, n = 1 ):
        '''skida prvih n znakova sa stoga
        '''
        pass
    
    
    def jest_prazan( self ):
        pass
