'''stablo

ovaj modul koristi za ispisivanje stabla

koristi za ispisiva
'''

from leksicka_jedinka import LeksickaJedinka
from unutarnji_cvor_stabla import UnutarnjiCvorStabla

class Stablo:
    
    def __init__( self, korijen ):
        
        self._korijen = korijen
    
    
    def ispisi_preorder( self, izlazni_tok ):
        '''pokreni ispis'''
        
        self._ispisuj( self._korijen, 0, izlazni_tok )
    
    
    def _ispisuj( self, cvor, dubina, izlazni_tok ):
        
        izlazni_tok.write( ' ' * dubina )
        
        if type( cvor ) == UnutarnjiCvorStabla:
            
            izlazni_tok.write( cvor.nezavrsni_znak + '\n' )
            
            for dijete in cvor.nezavrsni_znak:
                
                self._ispisuj( dijete, dubina + 1, izlazni_tok )
            
        elif type( cvor ) == LeksickaJedinka:
            
            if cvor.uniformni_znak != '$':
                # zavrsni znak
                
                izlazni_tok.write( cvor.uniformni_znak + ' ' )
                izlazni_tok.write( cvor.redak + ' ' )
                izlazni_tok.write( cvor.leksicka_jedinka + '\n' )
                
            else:
                # epsilon
                
                izlazni_tok.write( '$\n' )
            
        else:
            raise TypeError( 'krivi tip na stablu' )
