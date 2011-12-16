'''This is the main module of the lexycal analyzer implementation

created: 11. 10. 2011
Ivan Slijepcevic
'''

import sys
from lexycalanalyzer import LexycalAnalyzer
from automatparser import AutomatParser

if __name__ == '__main__':
    
    upute = 'analizator.upute'
    
    parser = AutomatParser( upute, sys.stdin )
    
    analyzer = parser.parse()
    
    analyzer.pokreni_analizu()
    analyzer.ispisi()
