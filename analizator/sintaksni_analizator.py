'''sintaksni analizator'''

import sys

from list_stabla import ListStabla
from unutarnji_cvor_stabla import UnutarnjiCvorStabla
from stog import Stog
from zajednicki.akcija import Akcija

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
    
    
    def analiziraj( self ):
        
        while( True ):
            
            trenutno_stanje = self.stog.dohvati_vrh()
            jedinka_s_ulaza = self.ulazni_niz[ self.index_parsiranja ]
            
            akcija = self.tablica_akcija[ trenutno_stanje ]
                                        .get( jedinka_s_ulaza.uniformni_znak,
                                            Akcija( 'odbaci' ) )
            
            if akcija.tip == 'pomakni':
                self.pomakni( jedinka_s_ulaza, akcija.vrijednost )
            
            elif akcija.tip == 'reduciraj':
                self.reduciraj( akcija.vrijenost )
            
            elif akcija.tip == 'prihvati':
                self.prihvati()
                break
            
            elif akcija.tip == 'odbaci':
                self.odbaci()
            
            else:
                raise KrivaAkcijaIznimka()
    
    
    def pomakni( self, leksicka_jedinka, novo_stanje ):
        '''tipovi parametara: LeksickaJedinka, int'''
        
        self.stog.stavi( leksicka_jedinka )
        self.stog.stavi( novo_stanje )
        self.index_parsiranja += 1
    
    
    def reduciraj( self, produkcija ):
        '''tip parametra: Produkcija'''
        
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
            self.stog.stavi( self.tablica_novo_stanje[ trenutno_stanje ]
                                                    .get( produkcija.desna_strana )
            
        else:
            # epsilon produkcija
            
    
    
    def prihvati( self ):
        
        
    
    
    def odbaci( self ):
        pass
