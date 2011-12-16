from analizator.zajednicki.greske import GreskaDka

class Prijelazi:
    '''prijelaz za automate, radi i za DKA i za eNKA
    '''
    
    def __init__( self, tip_iduce = int ):
        '''tip_iduce je tip podataka (ili klasa) za vrijednost prijelaza'''
        
        self._tip_iduce = tip_iduce
        self._prijelazi = {}
    
    
    def dodaj( self, index_stanja, znak, iduce ):
        
        if index_stanja not in self._prijelazi:
            self._prijelazi[ index_stanja ] = {}
        
        if self._tip_iduce == int:
            
            if type( iduce ) != int:
                raise TypeError( 'krivi tip vrijednosti prijelaza, ocekivan: ' + \
                            str( self._tip_iduce ) + '\tdobiven: ' + str( type( iduce )) )
            
            if znak in self._prijelazi[ index_stanja ]:
                raise GreskaDka( 'nedeterminizam: pokusaj dodavanja drugog ' + \
                                'stanja za neko stanje i znak' )
            
            self._prijelazi[ index_stanja ][ znak ] = iduce
        
        elif self._tip_iduce == set or self._tip_iduce == frozenset:
            
            if type( iduce ) == int:
                
                if znak not in self._prijelazi[ index_stanja ]:
                    self._prijelazi[ index_stanja ][ znak ] = self._tip_iduce([ iduce ])
                else:
                    self._prijelazi[ index_stanja ][ znak ] |= self._tip_iduce([ iduce ])
            
            else:   # valjda je predan neki set
                if znak not in self._prijelazi[ index_stanja ]:
                    self._prijelazi[ index_stanja ][ znak ] = iduce
                else:
                    self._prijelazi[ index_stanja ][ znak ] |= iduce
    
    
    def dohvati( self, index_stanja, znak ):
        
        if index_stanja not in self._prijelazi.keys():
            self._prijelazi[ index_stanja ] = {}
        
        if znak not in self._prijelazi[ index_stanja ].keys():
            self._prijelazi[ index_stanja ][ znak ] = self._prazno()
        
        return self._prijelazi[ index_stanja ][ znak ]
    
    
    def pisi_sve_prijelaze( self ):
        
        print( 'PRIJELAZI' )
        for index in self._prijelazi.keys():
            for znak in self._prijelazi[ index ].keys():
                print( index, type(index), znak, type(znak), '==', self._prijelazi[ index ][ znak ] )
    
    
    def _prazno( self ):
        
        tip = self._tip_iduce
        
        if tip == set or tip == list or tip == dict or tip == frozenset:
            return tip()
        
        if tip == int:
            return -1
        
        if tip == str:
            return ''
        
        return None
