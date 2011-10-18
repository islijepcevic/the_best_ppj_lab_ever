'''This is the main module of the lexycal analyzer implementation

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys
from lexycalanalyzer import LexycalAnalyzer
from automatparser import AutomatParser

if __name__ == '__main__':
    
    transition_table = '' #PUT PATH TO TRANSITION TABLE HERE
    
    # creation of lex. analyzer instance
    our_little_analyzer = LexycalAnalyzer( sys.stdin, transition_table,
        sys.stdout, sys.stderr )
    
    # create an instance of parser
    parser = AutomatParser( our_little_analyzer )
    
    # do the parsing
    parser.parse()
    
    # start the analysis of the parsed code
    our_little_analyzer.analyze()
