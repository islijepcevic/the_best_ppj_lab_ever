'''sintaksni analizator'''

import sys

from leksicka_jedinka import LeksickaJedinka
from unutarnji_cvor_stabla import UnutarnjiCvorStabla
from stog import Stog
from zajednicki.akcija import Akcija
from zajednicki.greske import GreskaAnaliziranja

class SintaksniAnalizator():
    
    def __init__( self, ulazni_niz, akcija, novo_stanje, pocetno_stanje,
                sinkronizacijski_znakovi, izlazni_tok = sys.stdout,
                tok_za_greske = sys.stderr ):
        
        # ULAZNI PROGRAM
        self.ulazni_niz = ulazni_niz    # niz instanci LeksickeJedinke
        self.index_parsiranja = 0
        
        # IZLAZVNI TOKOVI
        self.izlazni_tok = izlazni_tok
        self.tok_za_greske = tok_za_greske
        
        # TABLICE
        self.tablica_akcija = akcija
        self.tablica_novo_stanje = novo_stanje
        
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
        
        # PRACENJE REZULTATA
        self.niz_prihvacen = False  # postaje true kad je niz prihvacen bez
                                    # odbijanja
        self.niz_odbijen = False    # postaje true kad se niz odbije
    
    
    def analiziraj( self ):
        
        while( True ):
            
            trenutno_stanje = self.stog.dohvati_vrh()
            jedinka_s_ulaza = self.ulazni_niz[ self.index_parsiranja ]
            
            akcija = self.tablica_akcija[ trenutno_stanje ]
                                        .get( jedinka_s_ulaza.uniformni_znak,
                                            Akcija( 'odbaci' ) )
            
            if akcija.tip == 'pomakni':
                self._pomakni( jedinka_s_ulaza, akcija.vrijednost )
            
            elif akcija.tip == 'reduciraj':
                self._reduciraj( akcija.vrijenost )
            
            elif akcija.tip == 'prihvati':
                self._prihvati()
                break
            
            elif akcija.tip == 'odbaci':
                self._odbaci()
            
            else:
                raise GreskaAnaliziranja( 'nedozvoljen tip akcije u ' + \
                                        'tablici akcija' )
    
    
    def _pomakni( self, leksicka_jedinka, novo_stanje ):
        '''tipovi parametara: LeksickaJedinka, int'''
        
        self.stog.stavi( leksicka_jedinka )
        self.stog.stavi( novo_stanje )
        self.index_parsiranja += 1
    
    
    def _reduciraj( self, produkcija ):
        '''tip parametra: Produkcija'''
        
        trenutno_stanje = self.stog.dohvati_vrh()
        
        if produkcija.desna_strana != '$':
            # nije epsilon produkcija
            
            djeca_novog_cvora = []
            
            for i in range( len( produkcija.desna_strana ) ):
                
                self.stog.skini()
                
                djeca_novog_cvora.append( self.stog.dohvati_vrh() )
                self.stog.skini()
            
            djeca_novog_cvora.reverse()
            
            novi_cvor = UnutarnjiCvorStabla( produkcija.lijeva_strana,
                                            djeca_novog_cvora )
            
            trenutno_stanje = self.stog.dohvati_vrh()
            
            self.stog.stavi( novi_cvor )
            
        else:
            # epsilon produkcija
            
            djeca_novog_cvora = [ LeksickaJedinka( '$' ) ]
            
            self.stog.stavi( produkcija.lijeva_strana, djeca_novog_cvora )
        
        # stavljanje novog stanja
        try:
            novo_stanje = self.tablica_novo_stanje[ trenutno_stanje ]
                                                    [ produkcija.desna_strana ]
            
            self.stog.stavi( novo_stanje )
        
        except KeyError:
            raise GreskaAnaliziranja( 'pokusaj dohvacanja nepostojece ' + \
                                    'vrijednosti u tablici novo_stanje' )
    
    
    def _prihvati( self ):
        
        self.stog.skini()
        
        self.stablo = self.stog.dohvati_vrh()
        
        if not self.niz_odbijen:
            self.niz_prihvacen = True
    
    
    def _odbaci( self ):
        
        self.niz_odbijen = True
