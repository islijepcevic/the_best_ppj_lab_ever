'''This is the implementation of the lexycal analyzer automat

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys

class LexycalAnalyzer():
    '''class that contains the automat'''
    
    def __init__( self, code_input_stream, transition_table,
        outstream = sys.stdout, errstream = sys.stderr ):
        '''constructor
        
        arguments:
        code_input_stream - stream from where code comes from
        transition_table - file location of transition table
        outstream - stream to write output data (uniform unit table)
        errstream - stream to write code error data
        '''
        
        self.code_stream = code_input_stream
        self.transition_table = transition_table
        self.outstream = outstream
        self.errstream = errstream
        
        self.states = []
        self.initial_state = None
        self.acceptable_states = set([])
        self.transitions = {}
        
        self.input_sequence = ''
        
        # variables from the PPJ book
        self.start = 0
        self.end = -1
        self.last = 0
        self.realized_expression = ''
    
    
    def set_states( self ):
        pass
    
    
    def set_initial_state( self ):
        pass
    
    
    def set_acceptable_states( self ):
        pass
    
    
    def set_transitions( self ):
        # NOTE:
        # transitions are going to be dictionary
        # key will be the pair; (state, character)
        # value will be the list: [state, state, ...] # may be empty list
        pass
    
    
    def get_input_sequence( self ):
        pass
    
    
    def expand_to_e_environment( self ):
        '''expand states to the epsilon environment of current states'''
        pass
    
    
    def analyze( self ):
        '''starts the analyzing of the code'''
        pass
