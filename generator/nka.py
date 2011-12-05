'''nka model'''

from generator.dka import DKA

class NKA:
    
    def __init__( self, stanja, ulazni_znakovi, pocetno_stanje, prihvatljiva,
                prijelazi ):
        
        
        self.stanja             = set(stanja)           # skup LR1Stavki
        self.prihvatljiva       = set(prihvatljiva)     # skup LR1Stavki
        self.ulazni_znakovi     = set(ulazni_znakovi)   # skup stringova
        self.pocetno_stanje     = pocetno_stanje        # LR1Stavka
        self.prijelazi          = dict(prijelazi)       # rjecnik: kljuc = par (LR1Stavka, string)
                                                        # vrijednost = skup LR1Stavki
    
    
    def kreiraj_dka( self ):
        '''vraca instancu DKA
        generalno: knjiga utr, str 32
        MAK
        '''
        q0 = frozenset ({self.pocetno_stanje})
        
        stanjaDKA = set()
        stanjaDKA.add( q0 )
        
        postoji_neprihvatljivo = False
        
        neobradjena = set( )
        neobradjena.add( q0 )
        
        prijelaziDKA = dict()
        
        while len (neobradjena ) > 0:
            
            q1 = neobradjena.pop()
            
            for z in (self.ulazni_znakovi | set(['<<!>>']) ):
                
                new_q = set()
                
                for q in q1:    # q je stavka, q1 je skup stavki (frozenset)
                    
                    new_q  |= set(  self.prijelazi.get( (q, z), set() ) )
                
                new_q = frozenset( new_q )
                
                if new_q:
                    
                    if new_q not in stanjaDKA:
                        neobradjena.add( new_q )
                        stanjaDKA.add(new_q)
                    
                    prijelaziDKA[(frozenset(q1), z)] = new_q
                    
                else:
                    postoji_neprihvatljivo = True
                    prijelaziDKA[ (frozenset(q1), z) ] = frozenset([None])
        
        F = stanjaDKA.copy()
        
        if postoji_neprihvatljivo:
            stanjaDKA.add( frozenset([None]) )
        
        return DKA (stanjaDKA, self.ulazni_znakovi, q0, F, prijelaziDKA)