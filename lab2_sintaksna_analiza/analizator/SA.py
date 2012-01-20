'''main sintaksnog analizatora'''

import sys
import os

from parser_analizatora import ParserAnalizatora

src = os.path.dirname( os.path.realpath( __file__ ) ) + '/'

datoteka_tablice = src + 'tablice.upute'
datoteka_sinkronizacijski = src + 'sinkronizacijski.upute'

if __name__ == '__main__':
    
    parser = ParserAnalizatora( sys.stdin, datoteka_tablice,
                                datoteka_sinkronizacijski )
    
    #OTPRILIKE MAIN KOD
    automat = parser.parsiraj()
    automat.analiziraj()
    automat.ispisi_stablo()
