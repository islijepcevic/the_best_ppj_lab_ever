'''leksicka jedinka
predstavlja jedan ulazni znak za Parser
bit ce list u generativnom stablu
'''

class LeksickaJedinka:
    
    def __init__( self, uniformni_znak, redak = 0, leksicka_jedinka = '' ):
        
        self.uniformni_znak = uniformni_znak
        self.redak = redak
        self.leksicka_jedinka = leksicka_jedinka
