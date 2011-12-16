import sys
from datetime import datetime

from generator.parser import Parser
from generator.model_analizatora import ModelAnalizatora

datoteka_tablice = 'analizator/tablice.upute'
datoteka_sinkronizacijski = 'analizator/sinkronizacijski.upute'

if __name__ == '__main__':
    
    t1 = datetime.now()
    
    parser = Parser( sys.stdin )
    gramatika = parser.ucitaj_gramatiku()
    
    model = ModelAnalizatora( gramatika )
    
    # 
    model.ispisi_tablice( datoteka_tablice )
    
    # stvara datoteku sa sinkronizacijskim znakovima
    parser.ispisi_sinkronizacijske_znakove( datoteka_sinkronizacijski )
    
    t2 = datetime.now()
    print( t2 - t1 )
