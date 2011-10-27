import unittest
from tests.automatmodeltest import suite as amodelsuite

def run( suite ):
    unittest.TextTestRunner().run( suite() )

if __name__ == '__main__':
    
    run( amodelsuite )
