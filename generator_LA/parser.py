'''This is the input parser for the lexycal analyzer generator

created: 11. 10. 2011
Ivan Slijepcevic
'''

from generator.automatmodel import AutomatModel
from generator.regularexpression import RegularExpression
from generator.analyzerrule import AnalyzerRule

class Parser():
    '''This class ...'''
    
    def __init__( self, instream ):
        '''constructor'''
        
        self.input_stream = instream
        
        ''' Dictionary containg regexes with their respective names where the
        names are the keys, and correspoding regex is value
        '''
        self.regdefs = {}
        
        ''' Array containg all automata states '''
        self.states = []
        
        ''' Array containg all lexical units names '''
        self.lu_names = []
        
        ''' Array containing objects for all transition rules '''
        self.la_rules = []
    
    
    def parse( self ):
        
        la_definition_string = self.input_stream.read().split('\n')
        
        ''' First we split the file to its main parts: regexes, states,
        lexical units names and analyzer rules
        '''
        
        input_part = 'before'
        regular_definitions = []
        la_rules = []
        
        for line in la_definition_string:
            
            if line == '':
                continue
            
            if input_part == 'before':
                if line[0:2] != '%X':
                    # read regular definitions
                    regular_definitions.append( line )
                else:
                    input_part = 'after'
                    
                    # read states
                    self.states = line.split()[1:]
            else:
                if line[0:2] == '%L':
                    # read lexical units
                    self.lu_names = line.split()[1:]
                else:
                    # read rules
                    la_rules.append( line )
        
        # Save regdefs
        for rd in regular_definitions:
            key = rd.split('} ')[0][1:]
            val = RegularExpression( rd.split('} ')[1] )
            val = self._expand( val )
            self.regdefs[ key ] = val
        
        # Save rules
        lrstate = 'out'
        lastate = ''
        rx = ''
        args = [ '', False, '', -1 ]
        
        for line in la_rules:
            if lrstate == 'out':
                if line[0] == '<':
                    lastate = line[1:].split('>')[0]
                    pos_reg_begin = line.find( '>' ) + 1
                    rx = RegularExpression( line[ pos_reg_begin :] )
                    rx = self._expand( rx )
                elif line[0] == '{':
                    lrstate = 'in'
                else:
                    print('something wrong')
            else:
                if line != '}':
                    if line == 'NOVI_REDAK':
                        args[1] = True
                    elif line.split()[0] == 'UDJI_U_STANJE':
                        args[2] = line.split()[1]
                    elif line.split()[0] == 'VRATI_SE':
                        args[3] = int( line.split()[1] )
                    else:
                        args[0] = line
                else:
                    lrstate = 'out'
                    self.la_rules.append( AnalyzerRule( lastate, rx, args ) )
                    
                    lastate = ''
                    rx = ''
                    args = [ '', False, '', -1 ]
        
        return AutomatModel( self.regdefs, self.states, self.lu_names,
            self.la_rules )
    
    def _expand( self, rx ):
        '''expands regular definitions in regular expression to return only the
        regular expression'''
        
        # nadji reference
        start_point = 0
        while ( True ):
            
            start_pos = rx.find( '{', start_point )
            if start_pos == -1:
                break
            
            if not rx.jest_operator( start_pos ):
                start_point = start_pos + 1
                continue
            
            end_pos = rx.find( '}', start_point )
            
            wrapped_rx_name = rx[ ( start_pos + 1 ): end_pos ]
            
            rx = rx.zamijeni( start_pos, end_pos,
                self.regdefs[ wrapped_rx_name ] )
            
            start_point = end_pos + 1
        
        return rx
