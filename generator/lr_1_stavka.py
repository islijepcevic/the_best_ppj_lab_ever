'''LR(1) stavka'''

class LR1Stavka:
    
    def __init__( self, lijevo, prije, poslije, zapocinje ):
        
        self.lijeva_strana = lijevo
        self.desno_prije_tocke = prije
        self.desno_poslije_tocke = poslije
        self.skup_zapocinje = zapocinje
    
    
    def je_li_potpuna( self ):
        '''GOTOVO'''
        
        if self.desno_poslije_tocke == '':
            return True
        return False
    
    
    def __hash__( self ):
        
        za_hash = self.lijeva_strana
        za_hash += ':' + self.desno_prije_tocke
        za_hash += ':' + self.desno_poslije_tocke
        
        for znak in self.skup_zapocinje:
            za_hash += '^' + znak
        
        return hash( za_hash ) + len( self.skup_zapocinje )
    
    
    def __cmp__( self, other ):
        
        hash_self = self.__hash__()
        hash_other = other.__hash__()
        
        return hash_self - hash_other
