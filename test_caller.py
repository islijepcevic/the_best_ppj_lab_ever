import unittest
from tests.automatmodeltest import suite as amodelsuite
from tests.enkatest import suite as enkasuite

def run( suite ):
    unittest.TextTestRunner().run( suite() )

if __name__ == '__main__':
    
    #run( amodelsuite )
    run( enkasuite )
