import sys


def logicka_ekvivalencija( a, b ):
    
    if ( a and b ) or ( not a and not b ):
        return True
    return False


class TipPodatka:
    
    def __init__( self, const_kvalificiran = False ):
        
        self.const_kvalificiran = const_kvalificiran
    
    
    def je_li_const( self ):
        '''vraca true ako je tip brojevni const'''
        return self.const_kvalificiran


class JednostavniTip( TipPodatka ):
    '''brojevni tipovi, const brojevni tipovi, void'''
    
    def __init__( self, tip, const_kvalificiran = False ):
        
        if tip == 'void':
            const_kvalificiran = False
        
        TipPodatka.__init__( self, const_kvalificiran )
        
        self.tip = tip
    
    
    def je_li_svodivo( self, tip ):
        
        # TODO
        return True
    
    
    def je_li_void( self ):
        if self.tip == 'void':
            return True
        return False
    
    
    def __eq__( self, tip ):
        
        if type( tip ) != JednostavniTip:
            return False
        
        if self.je_li_void and tip.je_li_void:
            return True
        
        if self.tip == tip.tip:
            return logicka_ekvivalencija( self.const_kvalificiran,
                                        tip.const_kvalificiran )
        
        return False
    
    
    def __ne__( self, tip ):
        return not self.__eq__( tip )
    
    
    def __repr__( self ):
        ispis = self.tip
        if self.const_kvalificiran:
            ispis = 'const(' + ispis + ')'
        
        return ispis


class TipFunkcija( TipPodatka ):
    '''funkcija'''
    
    def __init__( self, domena, kodomena):
        
        TipPodatka.__init__( self, False )
        
        self.domena = domena
        self.kodomena = kodomena
    
    
    def je_li_svodivo( self, funkcija ):
        # mozda nepotrebno
        # TODO
        return True
    
    
    def je_li_domena_void( self ):
        if type( self.domena ) == JednostavniTip and self.domena.je_li_void():
            return True
        return False
    
    
    def __eq__( self, tip ):
        '''pazit na domenu (void ili lista parametara)'''
        
        if type( tip ) != TipFunkcija:
            return False
        
        if self.kodomena != tip.kodomena:
            return False
        
        if type( self.domena ) != type( tip.domena ):
            return False
        
        # void se ne treba usporedivati zasebno jer ako je domena void, onda je
        # dovoljno znati da su obje domene istog tipa (inace su lista tipova)
        if type( self.domena ) != list:
            return True
        
        # sada je domena zasigurno lista
        if len( self.domena ) != len( tip.domena ):
            return False
        
        for svoj, tudi in zip( self.domena, tip.domena ):
            if svoj != tudi:
                return False
        
        return True
    
    
    def __ne__( self, tip ):
        return not self.__eq__( tip )
    
    
    def __repr__( self ):
        return repr( self.domena ) + ' -> ' + repr( self.kodomena )


class TipNiz( TipPodatka ):
    
    def __init__( self, tip ):
        '''tip je JednostavniTip'''
        
        if type( tip ) != JednostavniTip:
            sys.stderr.write( 'krivi poziv TipNiz' )
        
        TipPodatka.__init__( self, tip.const_kvalificiran )
        
        self.tip = tip
    
    
    def je_li_svodivo( self, tip ):
        # TODO
        return True
    
    
    def __eq__( self, tip ):
        
        if type( tip ) != TipNiz:
            return False
        
        return self.tip == tip.tip
    
    
    def __ne__( self, tip ):
        return not self.__eq__( tip )
