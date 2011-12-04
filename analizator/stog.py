'''stog'''

class Stog:
    
    def __init__( self, pocetno_stanje = None ):
        
        self.stog = []
        
        if pocetno_stanje is not None:
            self.stavi( pocetno_stanje )
    
    
    def stavi( self, element ):
         '''stavi element na stog'''
         
         self.stog.append( element )
    
    
    def dohvati_vrh( self ):
        '''vrati element na vrhu stoga'''
        
        return self.stog[-1]
    
    
    def skini( self ):
        '''skini element s vrha stoga'''
        
        if self.jest_prazan():
            return GreskaNaStogu( 'pokusaj skidanja sa praznog stoga' )
        
        self.stog.pop()
    
    
    def jest_prazan( self ):
        '''vrati true ako je stog prazan'''
        
        if len( self.stog ) == 0:
            return True
        
        return False
