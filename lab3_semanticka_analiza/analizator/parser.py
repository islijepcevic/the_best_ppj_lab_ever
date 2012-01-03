'''parser generativnog stabla'''

import sys

from analizator.nezavrsni_znak import NezavrsniZnak
from analizator.leksicka_jedinka import LeksickaJedinka

class Parser:
    
    def __init__( self, ulazni_tok, tok_za_greske = sys.stderr ):
        
        self._ispisano_stablo = ulazni_tok.read() \
                                        .replace( '\r', '' ) \
                                        .split('\n')
        
        self._citani_redak = -1
        
        self._tok_za_greske = tok_za_greske
    
    
    def parsiraj( self ):
        '''vraca korijen stabla'''
        
        self._citani_redak = 0
        
        dubina = self._dohvati_dubinu()
        ime = self._dohvati_element()
        
        korijen = self._obradi( ime, dubina )
        
        return korijen
    
    
    def _obradi( self, ime_cvora, dubina_trenutni ):
        '''
        vraca obradivani nezavrsni znak
        index citanog retka se nalazi na retku trenutnog nezavrsnog znaka
        '''
        
        djeca = []
        
        while True:
            self._citani_redak += 1
            
            if self._zadnji_redak():
                self._citani_redak -= 1
                return NezavrsniZnak( ime_cvora, djeca )
            
            dubina_sljedeci = self._dohvati_dubinu()
            
            if dubina_sljedeci == dubina_trenutni + 1:
                
                element = self._dohvati_element()
                
                # je li zavrsni?
                if len( element.split(' ') ) > 1:
                    leksicka_jedinka = self._stvori_leksicku( element )
                    djeca.append( leksicka_jedinka )
                
                # nezavrsni znak ili '$'
                else:
                    # slucaj epsilon produkcija
                    if element == '$':
                        djeca.append( LeksickaJedinka( element ) )
                        continue
                    
                    # slucaj nezavrsni znak
                    nezavrsni_ispod = self._obradi( element, dubina_sljedeci )
                    djeca.append( nezavrsni_ispod )
                    
            else:
                
                if dubina_sljedeci > dubina_trenutni:
                    ispis = 'greska pri parsiranju stabla:  '
                    ispis += 'preveliki skok medu granama\n'
                    
                    ispis += 'redak u ispisu generativnog stabla: '
                    ispis += str( self._citani_redak ) + '\n'
                    
                    ispis += 'trenutni:: dubina: ' + str( dubina_trenutni ) + ' '
                    ispis += 'cvor: ' + ime_cvora + '\n'
                    ispis += 'sljedeci:: dubina: ' + str( dubina_sljedeci ) + ' '
                    ispis += 'redak: ' + self._ispisano_stablo[ self._citani_redak ] + '\n'
                    
                    ispis += '\n'
                    
                    self._tok_za_greske.write( ispis )
                    break
                
                self._citani_redak -= 1
                return NezavrsniZnak( ime_cvora, djeca )
        
        return NezavrsniZnak( ime_cvora, djeca + ['ERROR'] )
    
    
    def _dohvati_dubinu( self, odmak = 0 ):
        '''vraca broj razmaka ulaza, linije na koju pokazuje self._citani_redak
        ako se zeli neka linija dalje, zadaje se odmak od trenutnog citanog 
        retka
        '''
        
        brojac = 0
        redak = self._ispisano_stablo[ self._citani_redak ]
        
        while redak[ brojac ] == ' ':
            brojac += 1
        
        return brojac
    
    
    def _dohvati_element( self ):
        '''dohvati element stabla s ulaza na trenutno citanoj liniji'''
        
        return self._ispisano_stablo[ self._citani_redak ].lstrip()
    
    
    def _stvori_leksicku( self, element ):
        '''stvara leksicku jedinku iz linije stabla sa ulaza
        element je linija u ispisu stabla bez pocetnih razmaka
        '''
        
        dijelovi = element.split(' ')
        
        uniformni_znak = dijelovi[0]
        redak = dijelovi[1]
        jedinka = dijelovi[2]
        
        if len( dijelovi ) > 3:
            for dio in dijelovi[3:]:
                jedinka += ' ' + dio
        
        return LeksickaJedinka( uniformni_znak, redak, jedinka )
    
    
    def _zadnji_redak( self ):
        '''vraca True ako je trenutno citani redak zadnji'''
        
        if self._ispisano_stablo[ self._citani_redak ] == '':
            return True
        
        return False
