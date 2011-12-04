'''dka model'''

from analizator.zajednicki.greske import GreskaDka


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
    
    
    def _upariStanja (self, stanja):
        #print ("Stanja za parenje: " + str (stanja))
        parovi = list()
        
        if stanja:
            p = stanja.pop()
        
        if stanja:
            for q in stanja:
                parovi.append((p, q))
            
            parovi.extend(self._upariStanja(stanja))
        
        #print ("Vracam parove: " + str (parovi))
        return parovi
        
    def _jest_oznacen(self, oznake, p, q):
        for z in self.ulazni_znakovi:
            if oznake.get(((p, z), (q, z)), False):
                return True
            
        return False

    def _oznaci_listu (self, par, pList, oznake):
        for p in pList.get(par, []):
            if not oznake.get(p, False):
                oznake[p] = True
                self._oznaci_listu(p, pList, oznake)
    
    
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
        oznake = dict ()
        pList = dict ()
        
        neprihvatljiva = self.stanja - self.prihvatljiva
        
        print ("stanja: " + str (self.stanja) +
               "\nPrihvatljiva: " + str (self.prihvatljiva) +
               "\nNeprihvatljiva: " + str (neprihvatljiva))
        
        parovi = self._upariStanja(self.stanja.copy())
        
        
        
        ostali = []
        #korak 1
        for par in parovi:
            (p, q) = par
            if (p in self.prihvatljiva and q in neprihvatljiva
                or q in self.prihvatljiva and p in neprihvatljiva):
                
                oznake[par] = True
            else:
                ostali.append(par)
                
        
        for par in ostali:
            (p, q) = par
            for z in self.ulazni_znakovi:
                d1 = self.prijelazi.get((p, z), [])
                d2 = self.prijelazi.get((q, z), [])
                
                if d1 != d2 and d1 and d2:
                    if d1 >d2:
                        r = (d2, d1)
                    else:
                        r = (d1, d2)
                        
                        
                    if oznake.get(r, False):
                        oznake[par] = True
                        self._oznaci_listu(par, pList, oznake)
                        
                    else:
                        if pList.get (r, False):
                            pList[r].append(r)
                        else:
                            pList[r] = [par]
        
        
        '''
        ostali = []
        for par in parovi:
            (p, q) = par
            if ( p in self.prihvatljiva and q in neprihvatljiva
                 or q in self.prihvatljiva and p in neprihvatljiva):
                oznake[par] = True
            else:
                ostali.append (par)
                
        for par in ostali:
            for z in self.ulazni_znakovi:
                pr_p = (p, z)
                pr_q = (q, z)
                
                if (self.prijelazi.get(pr_p, 1) != self.prijelazi.get(pr_q, 0)):
                    if oznake.get (par):
                        self._oznaci_listu(par, pList, oznake) 
                    if pList.get (par, False):
                        pList[par].append(par)
                    else:
                        pList[par] = [par]
        
        '''

        
        '''
        for par in parovi:
            (p, q) = par
            
            for znak in self.znakovi:
                pr_p = (p, znak)
                pr_q = (q, znak)
                if self._jest_oznacen (uniq, p, q):
                    oznake[par] = True
                else:
                    
                        if (self.prijelazi.get(pr_p, 1) != self.prijelazi.get(pr_q, 0)):
                            if uniq.get ((pr_p, pr_q), False):
                                uniq[(pr_p, pr_q)].append(par)
                            else:
                                uniq[(pr_p, pr_q)] = [par]
           '''             
        
        
        
        
    
    
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
    
    
    

