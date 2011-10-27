import unittest
import random
import string

from generator.automatmodel import AutomatModel

class AutomatModelTestCase( unittest.TestCase ):
    
    def setUp( self ):
        
        with open( 'tests/automatmodel.data', 'r' ) as data_stream:
            test_data = data_stream.read().split('\n')
        
        self.models = []
        
        for line in test_data:
            if line == '' or line[0] == '#':
                continue
            
            if line[0] == 'D':
                regdef = eval( line[2:] )
            elif line[0] == 'S':
                stanja = eval( line[2:] )
            elif line[0] == 'L':
                lex = eval( line[2:] )
            elif line[0] == 'P':
                pravila = eval( line[2:] )
                model = AutomatModel( regdef, stanja, lex, pravila )
                self.models.append( model )
        
        with open('tests/regexautomat.data', 'r') as stream:
            test_data = stream.read().split('\n')
            
        self.regex = []
        self.automat = []
        self.abeceda = []
            
        for line in test_data:
            if line == '' or line[0] == '#':
                continue
                
            if line[0] == 'R':
                self.regex += [eval( line[2:] )]
            if line[0] == 'A':
                self.automat += [eval( line[2:] )]
            if line[0] == 'I':
                self.abeceda += [eval( line[2:] )]
    
    
    def tearDown( self ):
        
        for model in self.models:
            model.dispose()
            model = None
        
        del self.models[:]
    
    
    def test_dodavanje_prijalaza( self ):
        
        for model in self.models:
            tests_count = 100
            
            states = []
            chars = []
            next_states = []
            for i in range( tests_count ):
                states.append( random.randint( 0, 100 ) )
                chars.append( random.choice( string.ascii_lowercase ) )
                next_states.append( random.randint( 0, 100 ) )
                
                model.dodaj_prijelaz( states[i], next_states[i], chars[i] )
            
            for i in range( tests_count ):
                prijedena_stanja = model.prijelazi[ (states[i], chars[i] ) ]
                self.assertTrue( next_states[i] in prijedena_stanja )
    
    
    def test_dodavanje_epsilon( self ):
        
        for model in self.models:
            tests_count = 100
            
            states = []
            next_states = []
            for i in range( tests_count ):
                states.append( random.randint( 0, 100 ) )
                next_states.append( random.randint( 0, 100 ) )
                
                model.dodaj_epsilon_prijelaz( states[i], next_states[i] )
                
            for i in range( tests_count ):
                prijedena_stanja = model.prijelazi[ (states[i], '$' ) ]
                self.assertTrue( next_states[i] in prijedena_stanja )
    
    
    def _make_random_input( self, abeceda ):
        N = random.randint(1, 15)
        return ''.join(random.choice( abeceda ) for x in range(N))
    
    
    def epsilon( self, stanja, prijelazi ):
        
        backup = stanja.copy()
        while len(backup) != 0:
            stanje = backup.pop()
            for next in prijelazi.get((stanje, '$'), []):
                if next not in stanja:
                    stanja.add(next)
                    backup.add(next)
    
    
    def _run_automat( self, niz, pocetno, prijelazi, prihvatljivo ):
        tr_stanja = set([pocetno])
        self.epsilon( tr_stanja, prijelazi )
        
        print('niz ', niz, ':\t', tr_stanja, end='\t')
        for znak in niz:
            next = set([])
            for stanje in tr_stanja:
                next |= set( prijelazi.get((stanje, znak), []) )
                print( stanje, znak, prijelazi.get((stanje, znak), []), end=' ' )
            tr_stanja = next
            print(tr_stanja, end=' ')
            self.epsilon( tr_stanja, prijelazi )
            print(tr_stanja, end='\t')
            
        print()
        if prihvatljivo not in tr_stanja:
            return pocetno
        return prihvatljivo
    
    
    def test_make_automat( self ):
        
        tests_count = 50
        model = self.models[0]
        
        for i in range( len( self.regex ) ):
            l, d = model.pretvori( self.regex[i] )
            atm = self.automat[i]
            print('prijelazi:', model.prijelazi)
            print('prijelazi:', atm)
            for j in range( tests_count ):
                niz = self._make_random_input( self.abeceda[i] )
                testrez = self._run_automat( niz, l, model.prijelazi, d )
                myrez = self._run_automat( niz, 0, atm, 1 )
                
                print('izlaz', end = '\t')
                
                if myrez == 1:
                    print(1)
                    self.assertEqual( testrez, d )
                else:
                    print(0)
                    self.assertNotEqual( testrez, d )
                print()


def suite():
    tests = []
    #tests += ['test_dodavanje_prijalaza', 'test_dodavanje_epsilon']
    tests += ['test_make_automat']
    
    return unittest.TestSuite( list(map( AutomatModelTestCase, tests )) )

if __name__ == '__main__':
    unittest.main()