'''This is the main module of the lexycal analyzer implementation

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys
import os
from lexycalanalyzer import LexycalAnalyzer
from automatparser import AutomatParser

if __name__ == '__main__':
    
    src = os.path.dirname( os.path.realpath( __file__ ) ) + '/'
    upute = src + 'analizator.upute'
    
    parser = AutomatParser( upute, sys.stdin )
    
    analyzer = parser.parse()
    
    analyzer.pokreni_analizu()
    analyzer.ispisi()
