'''dka model'''

from analizator.zamjenjivi.greske import GreskaDka


def pronadji_index( niz, vrijednost ):
    '''ova funkcija ne bi trebala biti ovdje ni po kojem pogledu objektnog
    principa, ali sam vec stvarno jako umoran
    
    bilo bi puno bolje da sam naslijedio 'list' (kao niz) i tamo napisao ovo
    '''
    
    pocetak = 0
    kraj = len( niz )
    index = (pocetak + kraj) / 2
    
    while True:
        
        trenutni = niz[ index ]
        
        if trenutni < vrijednost:
            kraj = index
        elif trenutni > vrijednost:
            pocetak = index
        else:
            return index
        
        index_pom = index
        index = (pocetak + kraj) / 2
        
        if index == index_pom:
            raise GreskaDka( 'binary search zakazao' )


class DKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        self.stanja = stanja    # skup skupova LR1Stavki (i ako treba nesto dodatno za neprihvatljivo stanje)
                                # nako minimizacije stanja, ova varijabla postaje
                                # niz skupova LR1Stavki, a svugdje drugdje se za
                                # stanje koristi samo index tog niza
        
        self.prihvatljiva = prihvatljiva        # skup skupova LR1Stavki
        self.ulazni_znakovi = ulazni_znakovi    # skup stringova
        self.pocetno_stanje = pocetno_stanje    # LR1Stavka
        self.prijelazi = prijelazi      # rjecnik: kljuc = par (skup LR1Stavki, string)
                                        # vrijednost = skup LR1Stavki ->(ovdje to predstavlja jedno stanje)
        
        self._minimiziraj()
        self._pretvori_stanja_u_brojeve()
    
    
    def _minimiziraj( self ):
        '''minimiziranje stanja DKA
        GOTOVO
        '''
        
        #self._odbaci_nedohvatjiva()        # ne treba jer algoritam stvaranja DKA to vec radi
        self._spoji_istovjetna()
    
    
    def _odbaci_nedohvatjiva( self ):
        '''NE TREBA
        utr knjiga str 27 - 28
        cekaj s programiranjem ovoga dok se ne odluci kakvog ce oblika biti stanja
        MAK
        '''
        pass
    
    
    def _spoji_istovjetna( self ):
        '''utr knjiga str 26 - 27
        sada jos stanja nisu integeri, vec set setova
        
        MAK
        '''
        
        '''napomena: buduci da su uglavnom stanja tipa skup (set) za dobivanje
        stanja koja nisu prihvatljiva mozes napraviti skupovski Q\F'''
        
        '''pseudo u knjizi valja, mozda ga malo prosiris da pase za varijable i za
        sve slucajeve. ako ga zelis razumijet, kad se zavrtis u for petlji, 
        prvo shvati dio pod inace, a onda onaj if
        '''
        pass
    
    
    def _pretvori_stanja_u_brojeve( self ):
        '''IVAN'''
        
        stanja = prihvatljiva = set()
        
        if len( self.stanja ) == len( self.prihvatljiva ):
            stanja = prihvatljiva = sorted( list( self.stanja ) )
        
        elif len( self.stanja ) - 1 == len( self.prihvatljiva ):
            neprihvatljiva = stanja - prihvatljiva
            stanja = prihvatljiva = sorted( list( self.prihvatljiva ) )
            stanja.append( neprihvatljiva )
        
        else:
            raise GreskaDka( 'DKA je krivog oblika i ima vise od jednog neprihvatljivog stanja' )
        
        pocetno_stanje = pronadji_index( stanja, self.pocetno_stanje )
        
        novi_prijelazi = {}
        for kljuc in self.prijelazi.keys():
            
            # zamislimo: prijelaz(q, a) = r
            q = pronadji_index( stanja, kljuc[0] )
            a = kljuc[1]
            r = pronadji_index( stanja, self.prijelazi[ kljuc ] )
            
            if kljuc not in novi_prijelazi:
                novi_prijelazi[ (q, a) ] = r
            else:
                raise GreskaDka( 'DKA ima nedeterministicki prijelaz' )
        
        self.stanja = stanja
        self.prihvatljiva = prihvatljiva
        self.pocetno_stanje = pocetno_stanje
        self.prijelazi = novi_prijelazi
    
    

