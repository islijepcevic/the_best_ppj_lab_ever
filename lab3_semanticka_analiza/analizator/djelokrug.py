'''klasa kao tablica znakova za zadani djelokrug programa'''

class Djelokrug:
    
    def __init__( self, nad_djelokrug ):
        
        self.nad_djelokrug = nad_djelokrug
        
        self.tablica = {}   # k: ime, v: tip
    
    
    def dodaj( self, ime, tip ):
        '''dodavanje identifikatora'''
        self.tablica[ ime ] = tip
    
    
    def provjeri_funkciju( self, ime, tip ):
        '''ako postoji deklaracija ovog imena u ovom djelokrugu onda
        je pripadni tip te deklaracije (ovaj parametar) tip
        
        vraca true ako u OVOM djelokrugu postoji deklarirana FUNKCIJA s ovim
        imenom i ISTIM tipom (za tip funkcija postoji __eq__())
        
        takoder vraca true ako u OVOM djelokrugu ne postoji deklaracija ovog
        imena
        '''
        
        if not ime in self.tablica.keys():
            return True
        
        return self.tablica[ ime ] == tip
    
    
    def postoji_li_ime_lokalno( self, ime ):
        '''provjerava je li ime deklarirano u lokalnom (trenutnom) djelokrugu'''
        
        if ime in self.tablica.keys():
            return True
        return False
    
    
    def __repr__( self ):
        
        ispis = '{\n'
        for ime in self.tablica.keys():
            ispis += ime + ': ' + self.tablica[ime] + '\n'
        ispis += '}\n'
        
        return ispis
