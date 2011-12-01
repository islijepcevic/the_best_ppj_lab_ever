'''sintaksni analizator'''

import sys

from list_stabla import ListStabla
from unutarnji_cvor_stabla import UnutarnjiCvorStabla
from stog import Stog

class SintaksniAnalizator():
    
    def __init__( self, ulazni_niz, akcija, novo_stanje, pocetno_stanje,
                sinkronizacijski_znakovi, izlazni_tok = sys.stdout,
                tok_za_greske = sys.stderr ):
        
        # ULAZNI PROGRAM
        self.ulazni_niz = ulazni_niz    # niz instanci LeksickeJedinke
        
        # IZLAZVNI TOKOVI
        self.izlazni_tok = izlazni_tok
        self.tok_za_greske = tok_za_greske
        
        # TABLICE
        self.akcija = akcija
        self.novo_stanje = novo_stanje
        
        # STOG
        self.stog = Stog( pocetno_stanje )
        
        # GENERATIVNO STABLO
        self.generativno_stablo = None  # generativno stablo se gradi od listova
                                        # ova varijabla ce se tek na kraju
                                        # popuniti, kad se stablo izgradi i kad
                                        # bude postojao korijen te ce se iz nje
                                        # generirati ispis
        
        # SINKRONIZACIJSKI ZNAKOVI
        self.sinkronizacijski_znakovi = sinkronizacijski_znakovi
    
    
    def pokreni_analizu( self ):
        pass
