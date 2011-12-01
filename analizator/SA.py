'''main sintaksnog analizatora'''

import sys

from parser_analizatora import ParserAnalizatora

datoteka_tablice = 'tablice.upute'
datoteka_sinkronizacijski = 'sinkronizacijski.upute'

if __name__ == '__main__':
    
    parser = ParserAnalizatora( sys.stdin, datoteka_tablice,
                                datoteka_sinkronizacijski )
    
    #OTPRILIKE MAIN KOD
    automat = parser.parsiraj()
    automat.analiziraj()
    automat.ispisi_stablo()
