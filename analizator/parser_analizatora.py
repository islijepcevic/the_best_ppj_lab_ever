'''parser sintaksnog analizatora'''

from sintaksni_analizator import SintaksniAnalizator
from leksicka_jedinka import LeksickaJedinka
from zajednicki.produkcija import Produkcija
from zajednicki.akcija import Akcija

class ParserAnalizatora:
    '''parsira sve upute potrebne sintaksnom analizatoru
    
    1 - tablice akcija i novo stanje
    2 - sinkronizacijski znakovi
    '''
    
    def __init__( self, ulazni_tok_programa, put_do_tablica,
                put_do_sinkronizacijskih_znakova ):
        
        self.ulazni_tok = ulazni_tok
        self.put_do_tablica = put_do_tablica
        self.put_do_sinkronizacijskih_znakova = put_do_sinkronizacijskih_znakova
    
    
    def parsiraj( self ):
        '''IVAN'''
        
        # na kraj ulaznog niza dodati znak za kraj niza
        # treba biti instanca LeksickeJedinke sa atributom uniformni_znak
        # vrijednosti "<<!>>"
        pass
