'''This is the input parser for the lexycal analyzer generator

created: 11. 10. 2011
Ivan Slijepcevic
'''

class Parser():
    '''This class ...'''
    
    def __init__( self, instream ):
        '''constructor'''
        
        self.input_stream = instream
        
        # lista regdef. svaki clan liste bi bio nesto tipa n-torka:
        # (ime_def, izraz); moze i mala lista umjesto n-torke
        self.regular_definitions = []
        
        # ovdje ce ici 'desifrirane' reg_definicije
        self.regular_dict = {}
        
        #liste stringova
        self.analyzer_states = []
        self.lexical_units = []
        
        # lista objekata AnalyzerRule
        self.analyzer_rules = []
    
    
    def run():
        
        #procitaj ulaznu datoteku
        #ucitaj sve -> radi naredba stdin.read(); koristi self.input kao stream
        
        # popuni sve vrijednosti
        
        #obradi_reg_def (pomoc: ppj-labos-upute.pdf odjeljak 2.4.2 i slika 2.13)
        # kao objektnu paradigmu, predlazem da ovo implementiras u klasi
        # RegularExpression, u metodi get_rid_of_regdef (slobodno ju preimenujes)
        
        #kako preimenujes regdef, popuni 'ciste' regdef u dictionary 
        #(mozes i brisati listu putem); jer ce dict trebati kasnije, a ne list
        
        #za svaki objekt iz self.analyzer_rules
            #pozovi metodu koja ce u regularnom izrazu reg_def pretvoriti u izraz
            # opet mozes koristiti implementirano u koraku iznad
        
        #stvori automat( reg_def_dict, stanja, lex_unit, niz_pravila )
        
        #return automat
