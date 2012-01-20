'''semanticka analiza'''

import sys

from analizator.parser import Parser
from analizator.semanticki_analizator import SemantickiAnalizator

if __name__ == '__main__':
    
    generativno_stablo = Parser( sys.stdin ).parsiraj()
    
    semanticki_ispravno = SemantickiAnalizator( generativno_stablo, sys.stdout,
                                                sys.stderr ).analiziraj()
    
    if not semanticki_ispravno:
        sys.exit( 1 )
