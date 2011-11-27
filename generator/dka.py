'''dka model'''

class DKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        
        # KONSTRUKTOR MOZDA NECE IZGLEDATI OVAKO, TU SE JOS DVOUMIM KOJEG CE
        # TIPA BITI STANJA - SKUP LRSTAVKI ILI INTEGERI
        # ALI SIGURNO CE PRIMATI ULAZ KAKAV JE OPISAN GORNJOM DEFINICIJOM I 
        # DONJIM KOMENTARIMA!
        
        self.stanja = stanja                    # skup skupova LR1Stavki
        self.prihvatljiva = prihvatljiva        # skup skupova LR1Stavki
        self.ulazni_znakovi = ulazni_znakovi    # skup stringova
        self.pocetno_stanje = pocetno_stanje    # LR1Stavka
        self.prijelazi = prijelazi      # rjecnik: kljuc = par (LR1Stavka, string)
                                                # vrijednost = jedna LR1Stavka
        
        self._minimiziraj()
        # self._preramzmjesti ILI self._pretvori_u_brojeve
    
    
    def _minimiziraj( self ):
        '''minimiziranje stanja DKA
        GOTOVO
        '''
        
        self._odbaci_nedohvatjiva()
        self._spoji_istovjetna()
    
    
    def _odbaci_nedohvatjiva( self ):
        '''utr knjiga str 27 - 28
        cekaj s programiranjem ovoga dok se ne odluci kakvog ce oblika biti stanja
        MAK
        '''
        pass
    
    
    def _spoji_istovjetna( self ):
        '''utr knjiga str 26 - 27
        cekaj s programiranjem ovoga dok se ne odluci kakvog ce oblika biti stanja
        MAK
        '''
        
        '''napomena: buduci da su uglavnom stanja tipa skup (set) za dobivanje
        stanja koja nisu prihvatljiva mozes napraviti skupovski Q\F'''
        pass
