'''This is the implementation of the lexycal analyzer automat

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys

class LexycalAnalyzer():
    '''class that contains the automat'''
    
    def __init__( self, automat, ulazni_program, akcije
        izlazni_tok = sys.stdout, tok_za_greske = sys.stderr ):
        '''constructor
        
        arguments:
        code_input_stream - stream from where code comes from
        transition_table - file location of transition table
        outstream - stream to write output data (uniform unit table)
        errstream - stream to write code error data
        '''
        
        # stream variables
        self.izlazni_tok = outstream
        self.tok_za_greske = errstream
        
        self.automat = automat
        self.ulazni_program = ulazni_program
        
        self.stanja_analizatora #[string]
        self.tipovi_lex_jedinka #[string]
        
        self.niz_uniformnih_znakova #[(tip_lex_jedinke, redak, index_u_tablici_znakova)]
        self.tablica_znakova #[(tip_lex_jedinke, jedinka_kao_string)]
        
        self.brojac_linije = 1
        
        self.akcija = akcije #{ (stanje, izraz): [] }
        self.reg_izraz #[int]

        self.pocetak = 0
        self.posljednji = 0
        self.zavrsetak = -1
        self.izraz = 0
    


    def prepoznaj_izraz ( self ):
        P = self.automat.dohvati_presjek()
        R = self.automat.dohvati_trenutna()
        while R !=[]:
            if P == []: self.slucaj1(R,P)
            else: self.slucaj2(R,P)
        


    def slucaj1 ( self, R, P ):
        self.zavrsetak = self.zavrsetak + 1
        trenutni_znak = self.ulazni_program [self.zavrsetak]
        self.automat.promijeni_stanja( trenutni_znak )


    def slucaj2 ( self, R, P ):
        for i in range ( len( self.reg_izraz )):
            if self.reg_izraz[i] in P:
                self.izraz = i
                break
        self.posljednji = self.zavrsetak
        self.zavrsetak = self.zavrsetak + 1
        trenutni_znak = self.ulazni_program [self.zavrsetak]
        self.automat.promijeni_stanja( trenutni_znak )


        


