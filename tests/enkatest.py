
from analizator.eNKA import eNKA
import unittest

class ENkaTest( unittest.TestCase ):
    
    def setUp( self ):
        
        br_st = 4
        pocetno = 0
        prihv = set([ 2 ])
        prijelazi = { (0, '$'): [1], (1, '#'): [3], (3, '|'):[2] }
        
        self.automat = eNKA( br_st, pocetno, prihv, prijelazi )
        
        self.nizovi = []
        self.nizovi.append( ('#|', 1) )
        self.nizovi.append( ('#tt', 0) )
        self.nizovi.append( ('keuo|', 0) )
    
    
    def test_enka( self ):
        
        for niz, prihvatljivost in self.nizovi:
            
            self.automat.na_pocetak()
            
            for znak in niz:
                self.automat.promijeni_stanje( znak )
            
            prihv = self.automat.dohvati_presjek()
            if len(prihv) > 0:
                prihv = 1
            else:
                prihv = 0
            
            self.assertEqual( prihv, prihvatljivost )
    
def suite():
    tests = []
    #tests += ['test_dodavanje_prijalaza', 'test_dodavanje_epsilon']
    tests += ['test_enka']
    
    return unittest.TestSuite( list(map( ENkaTest, tests )) )

if __name__ == '__main__':
    unittest.main()
