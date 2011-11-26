'''This is the module that holds the implementation of regular expressions

created: 11. 10. 2011
Ivan Slijepcevic
'''

class RegularExpression( str ):
    '''class for handling regular expressions'''
    
    def __init__( self, expression ):
        '''constructor
        
        arguments:
        expression - the regular expression itself
        '''
        self.expression = expression
    
    
    def jest_operator( self, index ):
        br = 0
        while ( index - 1 >= 0 and self.expression[ index - 1 ] == '\\' ):
            br += 1
            index -= 1
        
        return br % 2 == 0
    
    
    def zamijeni( self, start, end, wrapped_rx ):
        '''u self regexu zamjenjuje regdef sa wrapped_rx'''
        
        return RegularExpression( self.expression[:start ] + '(' + \
            wrapped_rx + ')' + self.expression[ ( end + 1 ):] )
