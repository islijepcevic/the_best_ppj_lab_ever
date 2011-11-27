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
