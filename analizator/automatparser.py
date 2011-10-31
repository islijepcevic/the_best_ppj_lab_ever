'''This is the parser of input program to lexycal analyzer

created: 14. 10. 2011
Ivan Slijepcevic
'''

class AutomatParser():
    '''the implementation of CodeParser
    '''
    
    def __init__( self, lex_analyzer ):
        '''constructor
        
        arguments:
        lex_analyzer - the lexycal analyzer automat in which parsed data will be
            stored
        '''
        
        self.lex_analyzer = lex_analyzer
    
    
    def parse( self ):
        '''function that parses the code'''
        
        transition_stream = open( self.lex_analyzer.transition_table_path, 'r' )
        transition_table = transition_stream.read().split()
        transition_stream.close()
        
        ##############################
        # HERE PARSE THE LINES AND SAVE CONTENT TO THE ANALYZER
        # NEW METHODS WITHIN THE CLASS CAN BE CREATED AND CALLED
        ##############################
        