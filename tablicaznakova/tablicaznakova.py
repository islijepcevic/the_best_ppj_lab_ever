

class TablicaZnakova():
    
    def __init__( self ):
        
        # [( klasa_jedinke, jedinka )]
        self.tablica = []
    
    def dodaj( self, klasa, jedinka ):
        
        i = index = -1
        for kl, jed in self.tablica:
            i += 1
            if kl == klasa and jed == jedinka:
                index = i
                break
        else:
            index = len( self.tablica )
            self.tablaca.append( (klasa, jedinka) )
        
        return t
    
    
    def spremi_tablicu( self ):
        pass
    
    
    def ucitaj_tablicu( self ):
        pass
