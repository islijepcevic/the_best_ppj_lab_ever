'''This is the parser of input program to lexycal analyzer

created: 14. 10. 2011
Ivan Slijepcevic
'''
from eNKA import eNKA
from lexycalanalyzer import LexycalAnalyzer

class AutomatParser():
    '''the implementation of CodeParser
    '''
    
    
    def __init__( self, upute_path, code_stream ):
        '''constructor
        
        arguments:
        upute - path do datoteke s uputama za analizator
        '''
        
        self.upute_path = upute_path
        self.code_stream = code_stream
    
    
    def parse( self ):
        '''function that parses the code'''
        
        upute_stream = open( self.upute_path, 'r' )
        upute = upute_stream.read().split('\n')
        upute_stream.close()
        
        for line in upute:
            
            if line == '':
                continue
            
            if line[0] == 'R':
                reg_izrazi = eval( line[1:] )
                prihvatljiva_stanja = set( reg_izrazi )
            elif line[0] == 'A':
                akcije = eval( line[1:] )
            elif line[0] == 'S':
                broj_stanja = eval( line[1:] )
            elif line[0] == 'P':
                pocetno_stanje = eval( line[1:] )
            elif line[0] == 'T':
                prijelazi = eval( line[1:] )
            elif line[0] == 'Z':
                stanja = eval( line[1:] )
            elif line[0] == 'I':
                pocetno_stanje_la = line[1:]
            else:
                print( 'upute krive' )
        
        automat = eNKA( broj_stanja, pocetno_stanje, prihvatljiva_stanja,
            prijelazi )
        
        ulazni_kod = self.code_stream.read()
        
        return LexycalAnalyzer( automat, ulazni_kod, akcije, stanja, reg_izrazi,
            pocetno_stanje_la )
