'''This is module with the class that represents the rule of the lexycal
analyzer

created: 11. 10. 2011
Ivan Slijepcevic
'''

class AnalyzerRule():
    '''The model for the rule of the lexycal analyzer'''
    
    def __init__( self, state_name, regular_expression, actions ):
        '''constructor of the class
        
        arguments:
        state_name - the name of the state automat was in before rule is applied
        regular_expression - the regular expression, for the analyzed program,
            that indicates when rule should be applied
        actions - dictionary of actions to complete, possible keys:
            'lexical_unit'
            'new_line'
            'change_state_to'
            'go_back'
            VALUES IMPLEMENTATION IS YET TO BE DECIDED
        '''
        
        self.state_name = state_name
        
        self.regular_expression = '' # create the RegularExpression object
        
        # possible example of implementation
        self.lexical_unit = None
        self.new_line = False
        self.change_state_to = None
        self.go_back = None
