'''This is the parser of input program to lexycal analyzer

created: 14. 10. 2011
Ivan Slijepcevic
'''
from generator.analyzerrule import AnalyzerRule


class CodeParser():
    '''the implementation of CodeParser
    '''
    
    input_stream = ''
    
    ''' Dictionary containg regexes with their respective names where the
        names are the keys, and correspoding regex is value
    '''
    regexes = {}
    
    ''' Array containg all automata states '''
    states = []
    
    ''' Array containg all lexical units names '''
    lu_names = []
    
    ''' Array containing objects for all transition rules '''
    la_rules = []
    
    
    def __init__( self, definition ):
        '''constructor
        
        arguments:
        definition - escaped string containing the definition of the LA 
        '''
        
        #self.lex_analyzer = lex_analyzer
        self.set_input_stream(definition)
    
    def set_input_stream (self, stream):
        self.input_stream = stream
    
    def parse( self ):
        '''function that parses the code'''
        
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
        
        #transition_table = transition_stream.read().split()
        #transition_stream.close()
        
        # TODO: ne znam sto trebam spremati???
        ##############################
        # HERE PARSE THE LINES AND SAVE CONTENT TO THE ANALYZER
        # NEW METHODS WITHIN THE CLASS CAN BE CREATED AND CALLED
        ##############################
    
    ''' Generates analyzerRule objects from rules string
    '''
    def _gen_la_rules_ob (self, rules):
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
            
            
            
            

























