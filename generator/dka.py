'''dka model'''

from analizator.zajednicki.greske import GreskaDka


def pronadji_index( niz, vrijednost ):
    '''ova funkcija ne bi trebala biti ovdje ni po kojem pogledu objektnog
    principa, ali sam vec stvarno jako umoran
    
    bilo bi puno bolje da sam naslijedio 'list' (kao niz) i tamo napisao ovo
    '''
    
    pocetak = 0
    kraj = len( niz )
    index = (pocetak + kraj) // 2
    
    while True:
        
        trenutni = niz[ index ]
        
        if trenutni < vrijednost:
            kraj = index
        elif trenutni > vrijednost:
            pocetak = index
        else:
            return index - 1
        
        index_pom = index
        index = (pocetak + kraj) // 2
        
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
        
        #self._minimiziraj()
        self._pretvori_stanja_u_brojeve()
        
        '''
        print( 'PRIJELAZI' )
        for i in range( len( self.stanja ) ):
            for z in self.ulazni_znakovi:
                print( (i,z), '==', self.prijelazi[ (i,z) ] )
        print()
        '''
    
    
    def _minimiziraj( self ):
        '''minimiziranje stanja DKA
        GOTOVO
        '''
        
        # ne treba odbacivanje nedohvatljivih stanja jer algoritam stvaranja DKA to vec radi
        self._spoji_istovjetna()
    
    
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
        
        neprihvatljiva = self.stanja - self.prihvatljiva
        
        # inicijalizacija
        tablica_neistovjetnih = {}    #dict: key=stanje; 
                                            #value=dict: key=stanje; value = bool
        
        for stanje1 in self.stanja:
            
            tablica_neistovjetnih[ stanje1 ] = {}
            
            for stanje2 in self.stanja:
                
                if stanje1 >= stanje2:
                    continue
                if (stanje1 in neprihvatljiva and stanje2 in neprihvatljiva) or \
                    (stanje1 in self.prihvatljiva and stanje2 in self.prihvatljiva):
                    
                    # oba stanja su prihvatljiva ili neprihvatljiva => NE oznaci ih kao neistovjetna
                    tablica_neistovjetnih[ stanje1 ][ stanje2 ] = False
                else:
                    tablica_neistovjetnih[ stanje1 ][ stanje2 ] = True
        
        liste_uz_parove = {}
        
        for stanje1 in self.stanja:
            for stanje2 in self.stanja:
                
                if stanje1 >= stanje2:
                    continue
                
                for a in self.ulazni_znakovi:
                    novo1 = self.prijelazi[ stanje1, a ]
                    novo2 = self.prijelazi[ stanje2, a ]
                    
                    if novo1 == novo2:
                        continue
                    if novo1 > novo2:
                        tmp = novo1
                        novo1 = novo2
                        novo2 = tmp
                    
                    if tablica_neistovjetnih[ novo1 ][ novo2 ]:
                        tablica_neistovjetnih[ stanje1 ][ stanje2 ] = True
                        self._oznaci_rekurzivno( tablica_neistovjetnih, liste_uz_parove,
                                                stanje1, stanje2 )
                        break
                else:
                    for a in self.ulazni_znakovi:
                        novo1 = self.prijelazi[ stanje1, a ]
                        novo2 = self.prijelazi[ stanje2, a ]
                        
                        if novo1 == novo2:
                            continue
                        if novo1 > novo2:
                            tmp = novo1
                            novo1 = novo2
                            novo2 = tmp
                        
                        if (novo1, novo2) not in liste_uz_parove:
                            liste_uz_parove[ (novo1, novo2) ] = [ (stanje1, stanje2) ]
                        else:
                            liste_uz_parove[ (novo1, novo2) ].append( (stanje1, stanje2) )
        
        # sad su oznaceni - pronaci istovjetna
        istovjetna_stanja = []  # lista sa listom istovjetnih stanja
        for stanje1 in self.stanja:
            for stanje2 in self.stanja:
                if stanje1 >= stanje2:
                    continue
                
                if not tablica_stanja[ stanje1 ][ stanje2 ]:
                    continue
                
                self._dodaj_u_istovjetna( istovjetna, stanje1, stanje2 )
        
        # reprezentativna stanja su na nultom indexu u svakoj istovjetnoj skupini
        
        # makni dodatna stanja
        for skupina in istovjetna:
            for stanje in skupina[1:]:
                self.stanja.remove( stanje )
                self.prihvatljiva.discard( stanje )
        
        novi_prijelazi = {}
        for kljuc in self.prijelazi.keys():
            p = kljuc[0]
            a = kljuc[1]
            r = self.prijelazi[ kljuc ]
            
            for skupina in istovjetna:
                if p in skupina:
                    p = skupina[0]
                if r in skupina:
                    r = skupina[0]
            
            if (p, a) not in novi_prijelazi:
                novi_prijelazi[ (q, a) ] = r
            else:
                raise GreskaDka( 'DKA ima nedeterministicki prijelaz - minimizacija' )
        
        self.prijelazi = novi_prijelazi
    
    
    def _oznaci_rekurzivno( self, tablica_neistovjetnih, liste_uz_parove, p, q ):
        
        while lista_uz_parove[ (p, q) ]:
            (novi1, novi2) = lista_uz_parove[ (p, q) ].pop()
            tablica_neistovjetnih[ novi1, novi2 ] = True
            
            self._oznaci_rekurzivno( tablica_neistovjetnih, lista_uz_parove, novi1, novi2 )
    
    
    def _dodaj_u_istovjetna( self, istovjetna, s1, s2 ):
        
        if not istovjetna:
            istovjetna = [ [s1, s2] ]
        else:
            for i in range( len( istovjetna ) ):
                if s1 in istovjetna[i]:
                    if s1 == self.pocetno:
                        istovjetna[i].insert( 0, s2 )
                    else:
                        istovjetna[i].append( s2 )
                    break
                elif s2 in istovjetna[i]:
                    if s2 == self.pocetno:
                        istovjetna[i].insert( 0, s1 )
                    else:
                        istovjetna[i].append( s1 )
                    break
            else:
                istovjetna.append( [s1, s2] )
    
    
    def _pretvori_stanja_u_brojeve( self ):
        '''IVAN'''
        
        stanja = set()
        prihvatljiva = set()
        
        if len( self.stanja ) == len( self.prihvatljiva ):
            stanja = sorted( list( self.stanja ) )
            prihvatljiva = stanja[:]
        
        elif len( self.stanja ) - 1 == len( self.prihvatljiva ):
            neprihvatljiva = frozenset({None})
            prihvatljiva = sorted( list( self.prihvatljiva ) )
            stanja = prihvatljiva[:]
            stanja.append( neprihvatljiva )
            stanja = sorted( stanja )
        
        else:
            raise GreskaDka( 'DKA je krivog oblika i ima vise od jednog neprihvatljivog stanja' )
        
        pocetno_stanje = stanja.index( self.pocetno_stanje )#pronadji_index( stanja, self.pocetno_stanje )
        
        '''
        print()
        print( len( stanja ) )
        for stanje in stanja: print( stanje )
        print()
        print( 'PETLJA' )
        '''
        
        novi_prijelazi = {}
        for kljuc in self.prijelazi.keys():
            
            # zamislimo: prijelaz(q, a) = r
            q = stanja.index( kljuc[0] )#q = pronadji_index( stanja, kljuc[0] )
            a = kljuc[1]
            r = stanja.index( self.prijelazi[ kljuc ] )#pronadji_index( stanja, self.prijelazi[ kljuc ] )
            
            #print( q, a, r )
            
            if (q, a) not in novi_prijelazi:
                novi_prijelazi[ (q, a) ] = r
            else:
                ispis =  'DKA ima nedeterministicki prijelaz\n' + \
                    str( self.prijelazi[kljuc] ) + '\n' + \
                    str( novi_prijelazi[(q,a)] ) + '\n' + str(r) + '\n'
                #raise GreskaDka( ispis )
        
        self.stanja = stanja
        self.prihvatljiva = prihvatljiva
        self.pocetno_stanje = pocetno_stanje
        self.prijelazi = novi_prijelazi
    
    
    

