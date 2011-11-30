'''produkcija'''

class Produkcija:
    
    def __init__( self, lijevo, desno ):
        
        self.lijeva_strana = lijevo # string
        self.desna_strana = desno   # lista stringova!
    
    
    def __repr__( self ):
        '''metoda koja omogucava da se pri pozivu funkcije repr nad objektom ove
        klase pravilno izvrsi pretvorba u string, tako da kad se pozove eval,
        da se pravilno mogu ucitati sve vrijednosti
        
        IVAN
        '''
        return 'Produkcija("' + self.lijeva_strana + '","' + \
                str( self.desna_strana ) + '")'
