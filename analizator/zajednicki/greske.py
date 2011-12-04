'''greske i iznimke

GreskaDka
GreskaAnalizatora
GreskaNaStogu
'''

class Greska( Exception ):
    '''bazna greska za analizator'''
    pass


class GreskaDka( Greska ):
    '''greska na stogu'''
    
    def __init__( self, poruka ):
        
        self._poruka = poruka
    
    
    def __str__( self ):
        
        return self._poruka


class GreskaAnalizatora( Greska ):
    '''greska koja se dogodila prilikom analiziranja'''
    
    def __init__( self, poruka ):
        
        self._poruka = poruka
    
    
    def __str__( self ):
        
        return self._poruka


class GreskaNaStogu( Greska ):
    '''greska na stogu'''
    
    def __init__( self, poruka ):
        
        self._poruka = poruka
    
    
    def __str__( self ):
        
        return self._poruka
