'''parser generativnog stabla'''

from analizator.nezarvsni_znak import NezavrsniZnak
from analizator.leksicka_jedinka import LeksickaJedinka

class Parser:
    
    def __init__( self, ulazni_tok ):
        
        self._ispisano_stablo = ulazni_tok.read().replace( '\r', '' ).split('\n')
        
        self._citani_redak = -1
    
    
    def parsiraj( self ):
        '''vraca korijen stabla'''
        
        self._citani_redak = 0
        
        
    
    
    def _obradi( self, dubina_trenutni ):
        '''
        vraca djecu obradivanog cvora
        index citanog retka se nalazi na retku trenutnog nezavrsnog znaka
        '''
        
        djeca = []
        
        while True:
            self._citani_redak += 1
            
            dubina_sljedeci = self._dohvati_dubinu()
            
            if dubina_sljedeci == dubina_trenutni + 1:
                
                element = self._dohvati_element()
                
                # je li zavrsni?
                if len( element.split(' ') ) > 1:
                    leksicka_jedinka = self._stvori_leksicku()
                    djeca.append( leksicka_jedinka )
                
                # nije zavrsni znak -> cvor stabla
                else:
                    #obradi cvor ( dubina_sljedeci )
                    
            #elif dubina_sljedeci > dubina: NEPOTREBNO
                #obradi(sljedeci, dubina_sljedeci)
            #else
                #return djeca
        
        #return djeca
    
    
    def _dohvati_dubinu( self, odmak = 0 ):
        '''vraca broj razmaka ulaza, linije na koju pokazuje self._citani_redak
        ako se zeli neka linija dalje, zadaje se odmak od trenutnog citanog 
        retka
        '''
        pass
    
    
    def _dohvati_element( self ):
        '''dohvati element stabla s ulaza na trenutno citanoj liniji'''
        
        return self._ispisano_stablo[ self._citani_redak ].lstrip()
    
    
    def _stvori_leksicku( self, element ):
        '''stvara leksicku jedinku iz linije stabla sa ulaza'''
        
        dijelovi = element.split(' ')
        
        uniformni_znak = dijelovi[0]
        redak = dijelovi[1]
        jedinka = dijelovi[2]
        
        if len( dijelovi ) > 3:
            for dio in dijelovi[3:]:
                jedinka += ' ' + dio
        
        return LeksickaJedinka( uniformni_znak, redak, jedinka )
