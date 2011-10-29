'''This is module with the class that represents the rule of the lexycal
analyzer

created: 11. 10. 2011
Ivan Slijepcevic
'''

class AnalyzerRule():
    '''The model for the rule of the lexycal analyzer'''
    
    def __init__( self, state_name, regular_expression, arguments ):
        '''constructor of the class
        
        arguments:
        state_name - the name of the state automat was in before rule is applied
        regular_expression - the regular expression object, for the analyzed program,
            that indicates when rule should be applied
        arguments - list of arguments with their corresponding actions
        '''
        
        self.state_name = state_name
        
        self.regular_expression = regular_expression
        
        self.lexical_unit = None
        self.new_line = False
        self.change_state_to = None
        self.go_back = None
        
        self._parse_arguments (arguments)

        
    def _parse_arguments (self, arguments):
        self.lexical_unit = arguments.pop(0)
        if len (arguments) != 0:
            for arg in arguments:
                aname= arg.split()[0]
                
                if aname == 'UDJI_U_STANJE':
                    self.change_state_to = arg.split()[1]
                elif aname == 'NOVI_REDAK':
                    self.new_line = True
                elif aname == 'VRATI_SE':
                    self.go_back = arg.split()[1]
    
    def toString(self):
        return  ("---\ncurrentState: " + self.state_name + "\nregex: " +
                self.regular_expression +
                "\nLex unit: " + self.lexical_unit + '\nnew line: ' +
                str(self.new_line) + '\nchangeState: ' + str(self.change_state_to) +
                '\ngo Back: ' + str(self.go_back) + '\n---')
    #mak - slobodno dodaj funkcije koje ti trebaju u ovu klasu.