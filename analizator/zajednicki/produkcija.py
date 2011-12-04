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
                repr( self.desna_strana ) + '")'
    
    
    def __hash__( self ):
        
        za_hash = self.lijeva_strana
        
        for znak_gramatike in self.desna_strana:
            za_hash += ':' + znak_gramatike 
        
        return hash( za_hash )
    
    
    def __cmp__( self, other ):
        
        hash_self = self.__hash__()
        hash_other = other.__hash__()
        
        return hash_self - hash_other
