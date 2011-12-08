from analizator.zajednicki.greske import GreskaDka

class Prijelazi:
    '''prijelaz za automate, radi i za DKA i za eNKA
    '''
    
    def __init__( self, tip_iduce = type( int ) ):
        '''tip_iduce je tip podataka (ili klasa) za vrijednost prijelaza'''
        
        self._tip_iduce = tip_iduce
        self._prijelazi = {}
    
    
    def dodaj( self, index_stanja, znak, iduce ):
        
        if index_stanja not in self._prijelazi:
            self._prijelazi[ index_stanja ] = {}
        
        if type( self._tip_iduce ) == type( int ):
            
            if type( iduce ) != type( int ):
                raise TypeError( 'krivi tip vrijednosti prijelaza, ocekivan: ' + \
                            self._tip_iduce + '\tdobiven: ' + type( iduce ) )
            
            if znak in self._prijelazi[ index_stanja ]:
                raise GreskaDka( 'nedeterminizam: pokusaj dodavanja drugog ' + \
                                'stanja za neko stanje i znak' )
            
            self._prijelazi[ index_stanja ][ znak ] = iduce
        
        elif type( self._tip_iduce ) == type( set() ) or
            type( self._tip_iduce ) == type( frozenset() ):
            
            if type( iduce ) == type( int ):
                
                if znak not in self._prijelazi[ index_stanja ]:
                    self._prijelazi[ index_stanja ][ znak ] = self._tip_iduce( iduce )
                else:
                    self._prijelazi[ index_stanja ][ znak ] |= self._tip_iduce( iduce )
            
            else:   # valjda je predan neki set
                if znak not in self._prijelazi[ index_stanja ]:
                    self._prijelazi[ index_stanja ][ znak ] = iduce
                else:
                    self._prijelazi[ index_stanja ][ znak ] |= iduce
    
    
    def dohvati( self, index_stanja, znak ):
        
        if index_stanja not in self._prijelazi:
            self._prijelazi[ index_stanja ] = {}
        
        if znak not in self._prijelazi[ index_stanja ][ znak ]:
            return self._prazno()
        
        return self._prijelazi[ index_stanja ][ znak ]
    
    
    def _prazno( self ):
        
        tip = self._tip_iduce
        
        if tip == type( set() ) or tip == type( [] ) or tip == type( {} ) or
            tip == type( frozenset() ):
            
            return tip()
        
        if tip == type( int ):
            return -1
        
        if tip == type( str ):
            return ''
        
        return None
