'''LR(1) stavka'''

class LR1Stavka:
    
    def __init__( self, lijevo, prije, poslije, zapocinje,  ):
        
        self.lijeva_strana = lijevo         # string
        self.desno_prije_tocke = prije      # niz stringova
        self.desno_poslije_tocke = poslije  # niz stringova
        self.skup_zapocinje = frozenset( zapocinje )    # skup stringova
    
    
    def razrijesi_pr( self, druga ):
        '''rjesava pomakni/reduciraj proturjecje druge stavke prema sebi
        odnosno mice znak poslije tocke iz druge stavke iz svog skupa zapocinje
        (ako taj znak tamo postoji)
        
        vraca maknuti znak ako je maknut, inace None
        '''
        
        znak_iza_tocke = druga.desno_poslije_tocke[ 0 ]
        
        if znak_iza_tocke in self.skup_zapocinje:
            
            return LR1Stavka( self.lijeva_strana, self.desno_prije_tocke,
                            self.desno_poslije_tocke,
                            self.skup_zapocinje - { znak_iza_tocke } )
            
        return None
        
        '''
        # OVO MI SE CINI NEEFIKASNO, ALI JE TOCNO RADILO. ZATO TO JOS NECU POBRISATI
        for znak in self.skup_zapocinje:
            if znak == znak_iza_tocke:
                skup_za_maknuti |= znak
        
        self.skup_zapocinje -= skup_za_maknuti
        
        return skup_za_maknuti
        '''
    
    
    def je_li_potpuna( self ):
        '''GOTOVO'''
        
        if len( self.desno_poslije_tocke ) == 0:
            return True
        return False
    
    
    def _dodaj_u_string_za_hash( self, niz ):
        
        za_hash = ''
        
        for znak in niz:
            za_hash += '^' + znak
        
        return za_hash
    
    
    def __str__( self ):
        
        string = self.lijeva_strana + ' -> '
        string += str( self.desno_prije_tocke ) + ' * '
        string += str( self.desno_poslije_tocke ) + ', { '
        
        for znak in self.skup_zapocinje:
            string += znak + ', '
        string = string[:-2]
        
        string += ' }'
        
        return string
    
    
    def __repr__( self ):
        return self.__str__()
    
    
    def __hash__( self ):
        
        za_hash = self.lijeva_strana + \
        ':' + self._dodaj_u_string_za_hash( self.desno_prije_tocke ) + \
        ':' + self._dodaj_u_string_za_hash( self.desno_poslije_tocke ) + \
        ':' + self._dodaj_u_string_za_hash( self.skup_zapocinje )
        
        return hash( za_hash ) + len( self.skup_zapocinje )
    
    
    def __cmp__( self, other ):
        
        hash_self = self.__hash__()
        hash_other = other.__hash__()
        
        return hash_self - hash_other
    
    
    def __eq__( self, other ):
        
        if self.lijeva_strana == other.lijeva_strana and \
            self.desno_prije_tocke == other.desno_prije_tocke and \
            self.desno_poslije_tocke == other.desno_poslije_tocke and \
            self.skup_zapocinje == other.skup_zapocinje:
            
            return True
        
        return False
    
    
    def __ne__( self, other ):
        
        if self.lijeva_strana != other.lijeva_strana or \
            self.desno_prije_tocke != other.desno_prije_tocke or \
            self.desno_poslije_tocke != other.desno_poslije_tocke or \
            self.skup_zapocinje != other.skup_zapocinje:
            
            return True
        
        return False
