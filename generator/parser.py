'''This is the input parser for the lexycal analyzer generator

created: 11. 10. 2011
Ivan Slijepcevic
'''

class Parser():
    '''This class ...'''
    
    def __init__( self, definition):
        '''constructor'''
        
        self.input_stream = ''
        
        ''' Dictionary containg regexes with their respective names where the
        names are the keys, and correspoding regex is value
        '''
        self.regexes = {}
        
        ''' Array containg all automata states '''
        self.states = []
        
        ''' Array containg all lexical units names '''
        self.lu_names = []
        
        ''' Array containing objects for all transition rules '''
        self.la_rules = []
        
        # lista regdef. svaki clan liste bi bio nesto tipa n-torka:
        # (ime_def, izraz); moze i mala lista umjesto n-torke
        self.regular_definitions = []
        
        #self.lex_analyzer = lex_analyzer
        self.set_input_stream(definition)
    
    
    def set_input_stream (self, stream):
        self.input_stream = stream
    
    
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
    
    
    def parse( self ):
        
        #transition_stream = open( self.lex_analyzer.transition_table, 'r' )
        
        # FIXME: how to load la_definition_string
        #la_definition_string = transition_stream.read()
        la_definition_string = self.input_stream
        
        ''' First we split the file to its main parts: regexes, states,
        lexical units names and analyzer rules
        '''
        regexes_str = la_definition_string.split( '\n\n%X' )[0]
        states_str = la_definition_string.split( '%X' )[1].split('\n' )[0]
        lu_names_str = la_definition_string.split( '%L' )[1].split( '\n' )[0]
        la_rules_str = '\n' + la_definition_string.split( '%L' )[1].split( '\n\n' )[1]

        
        ''' Then we put them into an arrays
        '''
        
        ''' First regexes '''
        rx = regexes_str.split('\n')
        for r in rx:
            key = r.split('} ')[0][1:]
            val = r.split('} ')[1]
            self.regexes[key] = val
        
        ''' Then states '''
        self.states = states_str.split()
        
        ''' Lexical units names '''
        self.lu_names = lu_names_str.split()
        
        ''' Lexical analyzer rules '''
        rules = la_rules_str.split('\n}')
        rules.pop(-1)
        self.la_rules = self._gen_la_rules_ob (rules)
    
    
    def _gen_la_rules_ob (self, rules):
        ''' Generates analyzerRule objects from rules string'''
        
        #print (rules)
        analyzer_rules = []
        for rule in rules:
            state = rule.split('>')[0][2:]
            regex = rule.split('>')[1].splitlines()[0]
            arguments = rule.split('\n{\n')[1].split('\n')
                        
            #print (regex)
            #print (arguments)
            
            analyzer_rules.append(AnalyzerRule(state, regex, arguments))
        
        return analyzer_rules
