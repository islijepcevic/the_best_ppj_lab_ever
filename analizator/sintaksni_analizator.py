'''sintaksni analizator'''

import sys

from leksicka_jedinka import LeksickaJedinka
from unutarnji_cvor_stabla import UnutarnjiCvorStabla
from stog import Stog
from stablo import Stablo
from zajednicki.akcija import Akcija
from zajednicki.greske import GreskaAnaliziranja

class SintaksniAnalizator():
    
    def __init__( self, ulazni_niz, akcija, novo_stanje, pocetno_stanje,
                sinkronizacijski_znakovi, izlazni_tok = sys.stdout,
                tok_za_greske = sys.stderr ):
        
        # ULAZNI PROGRAM
        self._ulazni_niz = ulazni_niz    # niz instanci LeksickeJedinke
        self._index_parsiranja = 0
        
        # IZLAZVNI TOKOVI
        self._izlazni_tok = izlazni_tok
        self._tok_za_greske = tok_za_greske
        
        # TABLICE
        self.tablica_akcija = akcija
        self.tablica_novo_stanje = novo_stanje
        
        # STOG
        self._stog = Stog( pocetno_stanje )
        
        # GENERATIVNO STABLO
        self.generativno_stablo = None  # generativno stablo se gradi od listova
                                        # ova varijabla ce se tek na kraju
                                        # popuniti, kad se stablo izgradi i kad
                                        # bude postojao korijen te ce se iz nje
                                        # generirati ispis
        
        # SINKRONIZACIJSKI ZNAKOVI
        self._sinkronizacijski_znakovi = sinkronizacijski_znakovi
        
        # PRACENJE REZULTATA
        self._niz_prihvacen = False  # postaje true kad je niz prihvacen bez
                                    # odbijanja
        self._niz_odbijen = False    # postaje true kad se niz odbije
        
        self._niz_analiziran = False
    
    
    def analiziraj( self ):
        
        self._niz_analiziran
        
        while( True ):
            
            trenutno_stanje = self._stog.dohvati_vrh()
            jedinka_s_ulaza = self._ulazni_niz[ self._index_parsiranja ]
            
            akcija = self._dohvati_akciju( trenutno_stanje, jedinka_s_ulaza.uniformni_znak )
            
            if akcija.tip == 'pomakni':
                self._pomakni( jedinka_s_ulaza, akcija.vrijednost )
            
            elif akcija.tip == 'reduciraj':
                self._reduciraj( akcija.vrijenost )
            
            elif akcija.tip == 'prihvati':
                self._prihvati()
                break
            
            elif akcija.tip == 'odbaci':
                self._odbaci()
                self._ispisi_gresku()
                oporavak = self._oporavi()
                
                if not oporavak:
                    break
            
            else:
                raise GreskaAnaliziranja( 'nedozvoljen tip akcije u ' + \
                                        'tablici akcija' )
    
    
    def ispisi_stablo( self ):
        
        if not self._niz_analiziran:
            self.analiziraj()
        
        if self.generativno_stablo = None:
            return None
        
        #sljedece akcije ispisivanja stabla
    
    
    def _pomakni( self, leksicka_jedinka, novo_stanje ):
        '''tipovi parametara: LeksickaJedinka, int'''
        
        self._stog.stavi( leksicka_jedinka )
        self._stog.stavi( novo_stanje )
        self._index_parsiranja += 1
    
    
    def _reduciraj( self, produkcija ):
        '''tip parametra: Produkcija'''
        
        trenutno_stanje = self._stog.dohvati_vrh()
        
        if produkcija.desna_strana != '$':
            # nije epsilon produkcija
            
            djeca_novog_cvora = []
            
            for i in range( len( produkcija.desna_strana ) ):
                
                self._stog.skini()
                
                djeca_novog_cvora.append( self._stog.dohvati_vrh() )
                self._stog.skini()
            
            djeca_novog_cvora.reverse()
            
            novi_cvor = UnutarnjiCvorStabla( produkcija.lijeva_strana,
                                            djeca_novog_cvora )
            
            trenutno_stanje = self._stog.dohvati_vrh()
            
            self._stog.stavi( novi_cvor )
            
        else:
            # epsilon produkcija
            
            djeca_novog_cvora = [ LeksickaJedinka( '$' ) ]
            
            self._stog.stavi( produkcija.lijeva_strana, djeca_novog_cvora )
        
        # stavljanje novog stanja
        try:
            novo_stanje = self.tablica_novo_stanje[ trenutno_stanje ]
                                                    [ produkcija.desna_strana ]
            
            self._stog.stavi( novo_stanje )
        
        except KeyError:
            raise GreskaAnaliziranja( 'pokusaj dohvacanja nepostojece ' + \
                                    'vrijednosti u tablici novo_stanje' )
    
    
    def _prihvati( self ):
        
        self._stog.skini()
        
        self.generativno_stablo = Stablo( self._stog.dohvati_vrh() )
        
        if not self._niz_odbijen:
            self._niz_prihvacen = True
    
    
    def _odbaci( self ):
        self._niz_odbijen = True
    
    
    def _ispisi_gresku( self ):
        
        gresna_jedinka = self._ulazni_niz[ self._index_parsiranja ]
        
        redak_greske = gresna_jedinka.redak
        ocekivani_znakovi = self.tablica_akcija[ self._stog.dohvati_vrh() ].keys()
        procitani_znak = gresna_jedinka.uniformni_znak
        
        linija_analiziranog_koda = self._dohvati_liniju( redak_greske )
        
        from functools import reduce
        ocekivani_string = reduce( lambda x, y: str(x) + ', ' + str(y),
                                    ocekivani_znakovi )
        
        ispis = 'Greska u retku ' + str( redak_greske ) + ':\n'
        ispis += linija_analiziranog_koda + '\n'
        ispis += 'dobiven znak: ' + procitani_znak + '\n'
        ispis += 'ocekivani znak(ovi): ' + ocekivani_string + '\n'
        ispis += '\n'
        
        self.tok_za_greske.write( ispis )
    
    def _dohvati_liniju( self, redak ):
        
        prvi = zadnji = self._index_parsiranja
        
        while self._ulazni_niz[ prvi ].redak = redak:
            prvi -= 1
        
        while self._ulazni_niz[ zadnji ].redak = redak:
            zadnji += 1
        
        linija = ''
        kazaljka = prvi
        while kazaljka <= zadnji:
            
            linija += self._ulazni_niz[ kazaljka ].leksicka_jedinka
            kazaljka += 1
        
        return linija
    
    
    def _oporavi( self ):
        ''' oporavak od pogreske
        
        vraca boolean - true ako je oporavak uspio
        '''
        
        # pomakni se u nizu na prvi sinkronizacijski znak
        while not self._ulazni_niz[ self._index_parsiranja ].uniformni_znak in
                                                self._sinkronizacijski_znakovi:
            
            self._index_parsiranja += 1
            
            if self._index_parsiranja >= len( self._ulazni_niz ):
                
                # nije pronaden sinkronizacijski znak
                # vraca se false sa znacenjem da se prekida analiza
                # ne postoji generativno stablo
                return False
        
        while True:
            
            stanje = self._stog.dohvati_vrh()
            sinkronizacijski_znak = self._ulazni_niz[ self._index_parsiranja ]
            
            akcija = self._dohvati_akciju( stanje, sinkronizacijski_znak )
            
            if akcija.tip != 'odbaci':
                break
            
            # skini stanje
            self._stog.skini()
            
            if self._stog.jest_prazan():
                
                # nema mogucnosti za nastavak analize sa stanjima koja su bila
                # na stogu
                # analiza se prekida
                # ne postoji generativno stablo
                return False
            
            # skini cvor stabla / znak gramatike
            self._stog.skini()
        
        # vraca se true sa znacenjem da se analiza nastavlja
        return True
    
    
    def _dohvati_akciju( self, stanje, znak ):
        
        return self.tablica_akcija[ stanje ].get( znak, Akcija( 'odbaci' ) )
