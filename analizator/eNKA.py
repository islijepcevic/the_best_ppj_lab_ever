''''''

class eNKA:
    
    def __init__( self ):
        
        self.broj_stanja #int
        self.pocetno #int
        self.prihvatljiva #set([int])
        self.prijelazi #{ (int, char): [int] }
        self.trenutna_stanja #set([int])
        
        self.na_pocetak()

    def dohvati_trenutna_stanja(self):
        return self.trenutna_stanja

    def dohvati_presjek(self):
        return self.trenutna_stanja.intersection(self.prihvatljiva)

    def promijeni_stanje(self, znak):
        A=[]
        for i in (self.trenutna_stanja):
            A.append(self.prijelazi.get((i, znak),[]))
        self.trenutna_stanja=set(A)
        self.e_okruzenje()

    def e_okruzenje(self):
        S=self.trenutna_stanja.copy()
        while len(S)!=0:
            t=S.pop()
            L=self.prijelazi.get(t,'$')
            for v in (L):
                if v not in self.trenutna_stanja:
                    self.trenutna_stanja.add(v)
                    S.push(v)

    def na_pocetak(self):
        self.trenutna_stanja.clear()
        self.trenutna_stanja.add( self.pocetno )
        self.e_okruzenje()