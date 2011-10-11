'''This is the input parser for the lexycal analyzer generator

created: 11. 10. 2011
Ivan Slijepcevic
'''

class Parser():
    '''This class ...'''
    
    def __init__( self ):
        '''constructor'''
        
        # these variables might not be neccessary in the end because their value
        # might end up in the automat class immediately upon parsing
        # they are here just for the illustration what data will be parsed
        self.regular_definitions = [] # TO CONSIDER: make whole class for this
        self.analyzer_states = []
        self.lexical_units = []
        self.analyzer_rules = []
