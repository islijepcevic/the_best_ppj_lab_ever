'''parser sintaksnog analizatora'''

from sintaksni_analizator import SintaksniAnalizator
from leksicka_jedinka import LeksickaJedinka
from zajednicki.produkcija import Produkcija
from zajednicki.akcija import Akcija

class ParserAnalizatora:
    '''parsira sve upute potrebne sintaksnom analizatoru
    
    1 - tablice akcija i novo stanje
    2 - sinkronizacijski znakovi
    '''
    
    def __init__( self, ulazni_tok_programa, put_do_tablica,
                put_do_sinkronizacijskih_znakova ):
        
        self.ulazni_tok = ulazni_tok_programa
        self.put_do_tablica = put_do_tablica
        self.put_do_sinkronizacijskih_znakova = put_do_sinkronizacijskih_znakova
    
    
    def parsiraj( self ):
        '''IVAN'''
        
        (akcija, novo_stanje, poc_stog) = self._ucitaj_tablice()
        sinkronizacijski = self._ucitaj_sinkro()
        
        kod = self._ucitaj_kod()
        
        return SintaksniAnalizator( kod, akcija, novo_stanje, poc_stog, sinkronizacijski)
    
    
    def _ucitaj_tablice( self ):
        
        tok = open( self.put_do_tablica, 'r' )
        dat = tok.read().split('\n')
        tok.close()
        
        akcija = eval( dat[0] )
        novo_stanje = eval( dat[1] )
        poc_stog = eval( dat[2] )
        
        return (akcija, novo_stanje, poc_stog)
    
    
    def _ucitaj_sinkro( self ):
        tok = open( self.put_do_sinkronizacijskih_znakova, 'r' )
        dat = tok.read().split('\n')
        tok.close()
        
        return eval( dat[0] )
    
    
    def _ucitaj_kod( self ):
        
        kod = self.ulazni_tok.read().replace( '\r', '').split('\n')
        
        pravi_kod = []
        
        for line in kod:
            if line == '':
                continue
            
            line = line.split(' ')
            
            unif = line[0]
            redak = line[1]
            leksjed = ''
            for part in line[2:]:
                leksjed += part + ' '
            leksjed = leksjed[:-1]
            
            pravi_kod.append( LeksickaJedinka(unif, redak, leksjed) )
        
        pravi_kod.append( LeksickaJedinka('<<!>>') )
        for l in pravi_kod: print( l )
        print()
        return pravi_kod
