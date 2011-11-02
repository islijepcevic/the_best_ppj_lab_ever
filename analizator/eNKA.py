''''''

class eNKA:
    
    def __init__( self, broj_stanja, pocetno, prihvatljiva, prijelazi ):
        
        self.broj_stanja = broj_stanja #int
        self.pocetno = pocetno #int
        self.prihvatljiva = prihvatljiva #set([int])
        self.prijelazi = prijelazi #{ (int, char): [int] }
        
        self.trenutna_stanja = set([])
        
        self.na_pocetak()
        
    
    
    def dohvati_trenutna(self):
        #print( 'trenst:',self.trenutna_stanja )
        return self.trenutna_stanja
    
    
    def dohvati_presjek(self):
        #print( 'presj:', self.trenutna_stanja.intersection( self.prihvatljiva ) )
        return self.trenutna_stanja.intersection(self.prihvatljiva)
    
    
    def promijeni_stanje(self, znak):
        
        if len( znak ) > 0:
            A = set([])
            for stanje in self.trenutna_stanja:
                nova_stanja = set( self.prijelazi.get( (stanje, znak), [] ) )
                A.update( nova_stanja )
            self.trenutna_stanja = A
        
        self.e_okruzenje()
    
    
    def e_okruzenje(self):
        S = self.trenutna_stanja.copy()
        while len(S) != 0:
            t = S.pop()
            L = self.prijelazi.get( (t, 'epsilon'), [] )
            for v in (L):
                if v not in self.trenutna_stanja:
                    self.trenutna_stanja.add(v)
                    S.add(v)
            

    def na_pocetak(self):
        self.trenutna_stanja.clear()
        self.trenutna_stanja.add( self.pocetno )
        self.e_okruzenje()
        
        #print( 'init enka:', self.trenutna_stanja )
