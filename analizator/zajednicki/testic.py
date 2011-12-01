from produkcija import Produkcija

a = Produkcija( 'l', ['d','dd'] )
b = Produkcija( 'lll', ['ddd'] )
d = { 'idn': a, 'kon': b }

r = repr( d )
print( r, type(r) )

e = eval( r )
print( e, type(e) )
