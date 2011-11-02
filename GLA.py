'''This is the main module of the lexycal analyzer generator

The project is the 1st laboratory excercise for the PPJ subject at FER

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys

from generator.parser import Parser

if __name__ == '__main__':
    
    #create parser object (with sys.stdin)
    parser = Parser( sys.stdin )
    automat = parser.parse()
    
    automat.napravi_analizator()
