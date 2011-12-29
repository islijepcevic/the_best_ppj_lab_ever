'''parser generativnog stabla'''

from analizator.nezarvsni_znak import NezavrsniZnak
from analizator.leksicka_jedinka import LeksickaJedinka

class Parser:
    
    def __init__( self, ulazni_tok ):
        
        self._ispisano_stablo = ulazni_tok.read().replace( '\r', '' ).split('\n')
    
    
    def parsiraj( self ):
        
        citani_redak = 0
        
        