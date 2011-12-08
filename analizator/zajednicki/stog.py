'''stog'''

main =  len( __name__.split('.') )

if main == 3:
    from analizator.zajednicki.greske import GreskaNaStogu
else:
    from zajednicki.greske import GreskaNaStogu

class Stog1:
    
    def __init__( self, pocetno_stanje = None ):
        
        self.stog = []
        
        if pocetno_stanje is not None:
            self.stavi( pocetno_stanje )
    
    
    def stavi( self, element ):
         '''stavi element na stog'''
         
         self.stog.append( element )
    
    
    def dohvati_vrh( self ):
        '''vrati element na vrhu stoga'''
        
        if len( self.stog ) <= 0:
            raise GreskaNaStogu( 'pokusaj dohvacanja sa praznog stoga' )
        
        return self.stog[-1]
    
    
    def skini( self ):
        '''skini element s vrha stoga'''
        
        if self.jest_prazan():
            raise GreskaNaStogu( 'pokusaj skidanja sa praznog stoga' )
        
        self.stog.pop()
    
    
    def jest_prazan( self ):
        '''vrati true ako je stog prazan'''
        
        if len( self.stog ) == 0:
            return True
        
        return False


class Element:
    
    def __init__( self, vrijednost, sljedeci ):
        
        self.vrijednost = vrijednost
        self.sljedeci = sljedeci


class Stog2():
    
    def __init__( self, pocetna_vrijednost ):
        
        self.duljina = 1
        self.vrh = Element( pocetna_vrijednost, None )
    
    
    def stavi( self, element ):
        
        novi = Element( element, self.vrh )
        self.vrh = novi
        self.duljina += 1
    
    
    def skini( self ):
        
        if self.vrh is None:
            raise GreskaNaStogu( 'pokusaj skidanja sa praznog stoga' )
        
        self.vrh = self.vrh.sljedeci
        self.duljina -= 1
    
    
    def dohvati_vrh( self ):
        
        if self.vrh is None:
            raise GreskaNaStogu( 'pokusaj dohvacanja sa praznog stoga' )
        
        return self.vrh.vrijednost
    
    
    def jest_prazan( self ):
        
        if self.vrh is None:
            return True
        
        return False

Stog = Stog2
