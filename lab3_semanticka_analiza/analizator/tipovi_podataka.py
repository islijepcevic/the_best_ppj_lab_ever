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
        
        if type( tip ) != JednostavniTip:
            return False
        
        # jedina moguca razlika u const; to je svodivo
        if self.tip == tip.tip:
            return True
        
        # void moze ostati samo void, int ne ide u nista nize
        elif self.tip == 'void' or tip.tip == 'void' or self.tip == 'int':
            return False
        
        
        return True
    
    
    def je_li_svodivo_eksplicitno( self, tip ):
        
        if type( tip ) != JednostavniTip:
            return False
        
        if self.tip == tip.tip:
            return True
        
        if tip.tip == 'void':
            return False
        
        return True
    
    
    def je_li_void( self ):
        if self.tip == 'void':
            return True
        return False
    
    
    def je_li_l_izraz( self ):
        '''vraca true ako tip moze biti l-izraz'''
        return not self.je_li_void() and not self.je_li_const()
    
    
    def __eq__( self, tip ):
        
        if type( tip ) != JednostavniTip:
            return False
        
        if self.je_li_void() and tip.je_li_void():
            return True
        
        if self.tip == tip.tip:
            return logicka_ekvivalencija( self.const_kvalificiran,
                                        tip.const_kvalificiran )
        
        return False
    
    
    def __ne__( self, tip ):
        return not self.__eq__( tip )
    
    
    def __hash__( self ):
        
        totalni_hash = 0
        
        if self.tip == 'char':
            totalni_hash = 1
        elif self.tip == 'int':
            totalni_hash = 2
        
        if self.je_li_const():
            totalni_hash += 2
        
        return totalni_hash
    
    
    def __repr__( self ):
        ispis = self.tip
        if self.je_li_const():
            ispis = 'const(' + ispis + ')'
        
        return ispis


class TipFunkcija( TipPodatka ):
    '''funkcija'''
    
    def __init__( self, domena, kodomena):
        
        TipPodatka.__init__( self, False )
        
        self.domena = domena
        self.kodomena = kodomena
    
    
    def je_li_svodivo( self, funkcija ):
        '''mislim da se ovo nikad ne poziva, ipak ovdje je logika'''
        
        if type( funkcija ) != TipFunkcija:
            return False
        
        # mislim da je ovaj uvjet nepotreban, mozda ga treba maknuti
        if not self.kodomena.je_li_svodivo( funkcija.kodomena ):
            return False
        
        if len( self.domena ) != len( funkcija.domena ):
            return False
        
        for svoj, tudi in zip( self.domena, funkcija.domena ):
            
            if not svoj.je_li_svodivo( tudi ):
                return False
        
        return True
    
    
    def je_li_svodivo_eksplicitno( self, tip ):
        
        #if type( tip ) != JednostavniTip:
            #return False
        
        #return self.kodomena.je_li_svodivo_eksplicitno( tip )
        
        # ako sam shvatio upute, onda je ovo tocno
        return False
    
    
    def je_li_domena_void( self ):
        if type( self.domena ) == JednostavniTip and self.domena.je_li_void():
            return True
        return False
    
    
    def je_li_l_izraz( self ):
        '''vraca true ako tip moze biti l-izraz'''
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
    
    
    def __hash__( self ):
        
        totalni_hash = hash( self.kodomena )
        
        prim = 13
        i = 0
        
        if type( self.domena ) == list:
            
            for tip in self.domena:
                i += 1
                totalni_hash += i * prim + hash( tip )
        
        return totalni_hash
    
    
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
        '''moze li se self.tip svesti na tip?'''
        
        if type( tip ) != TipNiz:
            return False
        
        if self.je_li_const() and not tip.je_li_const():
            return False
        
        return self.tip.je_li_svodivo( tip.tip )
    
    
    def je_li_svodivo_eksplicitno( self, tip ):
        '''po uputi, ovo se ne smije'''
        return False
    
    
    def je_li_l_izraz( self ):
        '''vraca true ako tip moze biti l-izraz'''
        return False
    
    
    def __eq__( self, tip ):
        
        if type( tip ) != TipNiz:
            return False
        
        return self.tip == tip.tip
    
    
    def __ne__( self, tip ):
        return not self.__eq__( tip )
    
    
    def __hash__( self ):
        
        return hash( self.tip ) + 5
    
    
    def __repr__( self ):
        return 'niz( ' + repr( self.tip ) + ' )'
