'''This is the implementation of the lexycal analyzer automat

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys

class LexycalAnalyzer():
    '''class that contains the automat'''
    
    def __init__( self, automat, ulazni_program, akcije, stanja_analizatora,
        reg_izrazi, pocetno_stanje, izlazni_tok = sys.stdout,
        tok_za_greske = sys.stderr ):
        '''constructor
        
        arguments:
        code_input_stream - stream from where code comes from
        transition_table - file location of transition table
        outstream - stream to write output data (uniform unit table)
        errstream - stream to write code error data
        '''
        
        # stream variables
        self.izlazni_tok = izlazni_tok
        self.tok_za_greske = tok_za_greske
        
        self.automat = automat
        self.ulazni_program = ulazni_program
        
        #self.tipovi_lex_jedinka #[string]
        #self.lista_stanja_analizatora
        
        self.akcije = akcije #{ (stanje, izraz): [] }
        
        # regularni izrazi poredani kao u ulaznoj datoteci, vrijednosti su prihv. stanja automata
        self.reg_izrazi = reg_izrazi  #[int]
        # pocetna stanja svakog prijelaza poredana kao regularni izrazi
        self.stanja_analizatora = stanja_analizatora #[string]
        
        self.pocetak = 0
        self.posljednji = 0
        self.zavrsetak = -1
        self.izraz = -1
        
        self.brojac_linije = 1
        
        self.niz_uniformnih_znakova = [] #[(tip_lex_jedinke, redak, index_u_tablici_znakova)]
        self.tablica_znakova = []#[(tip_lex_jedinke, jedinka_kao_string)]
        
        self.trenutno_stanje = pocetno_stanje
    
    
    def pokreni_analizu( self ):
        
        while ( self.pocetak < len( self.ulazni_program ) ):
            
            self.prepoznaj_izraz()
            
            if self.izraz == -1:
                self.oporavak()
            else:
                self.odredi_jedinku()
    
    
    def prepoznaj_izraz ( self ):
        P = self.automat.dohvati_presjek()
        R = self.automat.dohvati_trenutna()
        while len(R) > 0:
            
            if P == []:
                self.slucaj1()
            else:
                self.slucaj2( P )
            
            if self.zavrsetak == len( self.ulazni_program ):
                break
            
            P = self.automat.dohvati_presjek()
            R = self.automat.dohvati_trenutna()
    
    
    def slucaj1 ( self ):
        self.zavrsetak += 1
        if self.zavrsetak == len( self.ulazni_program ):
            trenutni_znak = ''
        else:
            trenutni_znak = self.ulazni_program[ self.zavrsetak ]
        #print( 'trenutni znak', trenutni_znak )
        self.automat.promijeni_stanje( trenutni_znak )
    
    
    def slucaj2 ( self, P ):
        for i in range( len( self.reg_izrazi ) ):
            
            reg_izraz = self.reg_izrazi[i]
            if self.reg_izrazi[i] in P and \
                self.trenutno_stanje == self.stanja_analizatora[i]:
                
                self.izraz = i
                self.posljednji = self.zavrsetak
                break
        
        self.slucaj1()
    
    
    def oporavak(self):
        self.tok_za_greske.write( self.ulazni_program[ self.pocetak ] )
        
        self.zavrsetak = self.pocetak
        self.pocetak = self.pocetak + 1
        self.automat.na_pocetak()
    
    
    def odredi_jedinku ( self ):
        reg_izraz = self.reg_izrazi[ self.izraz ]
        pravilo = self.akcije[(self.trenutno_stanje, reg_izraz)]
        
        klasa = pravilo[0]
        
        ime_stanja = pravilo[2]
        
        if pravilo[3] != -1:
            self.posljednji = self.pocetak + pravilo[3] - 1
        
        leksicka_jedinka = self.ulazni_program[ self.pocetak : self.posljednji + 1 ]
        
        self.izraz = -1
        self.pocetak = self.posljednji + 1
        self.zavrsetak = self.posljednji
        
        if ime_stanja != '':
            self.trenutno_stanje = ime_stanja
        
        if klasa != '-':
            self.dodaj_u_tablicu( klasa, leksicka_jedinka )
        
        if pravilo[1] == True:
            self.brojac_linije += 1
        
        self.automat.na_pocetak()
        
        #print( klasa, ime_stanja, ':' +leksicka_jedinka + ':', self.brojac_linije )
    
    
    def dodaj_u_tablicu(self, klasa, leksicka_jedinka):
        for p in range(len(self.tablica_znakova)):
            if self.tablica_znakova[p][0]==klasa and self.tablica_znakova==leksicka_jedinka:
                t=p
                break
        else:
            self.tablica_znakova.append((klasa, leksicka_jedinka))
            t=len(self.tablica_znakova)-1
        
        #klasa, redak, index
        self.niz_uniformnih_znakova.append((klasa, self.brojac_linije, t))
    
    
    def ispisi( self ):
        
        ispis = ''
        
        for klasa, redak, index in self.niz_uniformnih_znakova:
            
            jedinka = self.tablica_znakova[ index ][1]
            ispis += klasa + ' ' + str(redak) + ' ' + jedinka + '\n'
        
        #print (self.niz_uniformnih_znakova )
        self.izlazni_tok.write( ispis )
