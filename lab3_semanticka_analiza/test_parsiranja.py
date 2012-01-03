from analizator.parser import Parser
from analizator.nezavrsni_znak import NezavrsniZnak

def ispisi( cvor, dubina = 0 ):
    print( dubina, cvor.nezavrsni_znak, cvor.djeca )
    for dijete in cvor.djeca:
        if type( dijete ) == NezavrsniZnak:
            ispisi( dijete, dubina + 1 )
        #elif type(dijete) == str:
            #print( dubina, dijete )
        else:
            print( dubina + 1, dijete.uniformni_znak, dijete.redak,
                dijete.leksicka_jedinka )


# samo na mojem kompu - IVAN
put = "/home/ivan/semestar/PPJ/lab/test_primjeri/langdefs_sluzbeno/"

tok = open( put + 'minusLang.out', 'r' )

generativno_stablo = Parser( tok ).parsiraj()

tok.close()

ispisi( generativno_stablo )
