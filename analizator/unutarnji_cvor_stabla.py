'''unutarnji cvor generativnog stabla'''

class UnutarnjiCvorStabla():
    
    def __init__( self, nezavrsni_znak, djeca ):
        
        self.nezavrsni_znak = nezavrsni_znak
        
        self.djeca = djeca
    
    
    def __repr__( self ):
        return '(' + self.nezavrsni_znak + ')'
    
    def __str__( self ):
        return '(' + self.nezavrsni_znak + ')'
    
    # funkcije za postavljanje, dohvacanje djece i slicno sto ce trebati
