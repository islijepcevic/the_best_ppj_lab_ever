import sys

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
        
        # TODO
        return True
    
    
    def je_li_domena_void( self ):
        if type( self.domena ) == JednostavniTip and self.domena.je_li_void():
            return True
        return False
    
    
    def __eq__( self, tip ):
        '''pazit na domenu (void ili lista parametara)'''
        # TODO
        return True
    
    
    def __repr__( self ):
        return repr( self.domena ) + ' -> ' + repr( self.kodomena )


class TipNiz( TipPodatka ):
    
    def __init__( self, tip ):
        '''tip je JednostavniTip'''
        
        if type( tip ) != JednostavniTip:
            sys.stderr.write( 'krivi poziv TipNiz' )
        
        TipPodatka.__init__( self, tip.const_kvalificiran )
        
        self.tip = tip
