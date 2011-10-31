import unittest
import string

from analizator.automatparser import CodeParser

inputStream = """{prviTest} test|Regularnih|Definicija
{nadov} nestoZaNadovezivanje
{kleen} nestoZaKleena*
{zag} zagrade(a|b)*
{nestoSeps} (a|b|$|d|e)*

%X S_pocetno S_komentar S_nesto

%L IDN numConst strConst OP_neki

<S_pocetno>#\|
{
-
UDJI_U_STANJE S_komentar
}
<S_komentar>\|#
{
-
UDJI_U_STANJE S_pocetno
NOVI_REDAK
VRATI_SE 4
}
<S_komentar>\\n
{
-
NOVI_REDAK
}"""

class ParserTestCase( unittest.TestCase):
    
    def test_parse (self):
        parser = CodeParser (None)
        parser.set_input_stream(inputStream)
        parser.parse()
        
        #print (parser.input_stream)
        #print (parser.la_rules_str)
        #print (parser.regexes_str)
        #print (parser.regexes)
        #for a in parser.la_rules_str.split('\n'):
        #    print (a)
        #print (parser.la_rules_str.split('}\n'))
        
        print (parser.regexes)
        print (parser.states)
        print (parser.lu_names)
        print (parser.la_rules)
        for rule in parser.la_rules:
            print (rule.toString())
        





def suite():
    tests = []
    #tests += ['test_dodavanje_prijalaza', 'test_dodavanje_epsilon']
    tests += [inputStream]
    
    return unittest.TestSuite( list(map( ParserTestCase, tests )) )

if __name__ == '__main__':
    unittest.main()