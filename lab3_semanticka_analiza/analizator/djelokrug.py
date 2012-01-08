'''klasa kao tablica znakova za zadani djelokrug programa'''

class Djelokrug:
    
    def __init__( self, nad_djelokrug = None, petlja = False, povrat = None ):
        
        self.nad_djelokrug = nad_djelokrug
        
        self.tablica = {}   # k: ime, v: tip
        
        # True ako je djelokrug direktno unutar neke petlje,
        # pretrazivati rekurzivno
        self.petlja = petlja
        
        # ako je blok tijelo neke funkcije
        # onda je povrat tip povratnog parametra (kodomena), inace None
        # pretrazivati rekurzivno
        self.povrat = povrat
    
    
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
    
    
    def je_li_deklarirano( self, ime ):
        '''provjerava postoji li ime deklarirano, pocevsi od lokalnog djelokruga
        i provjeravati sve do globalnog'''
        
        if ime in self.tablica:
            return True
        
        if self.nad_djelokrug is None:
            return False
        
        return self.nad_djelokrug.je_li_deklarirano( ime )
    
    
    def dohvati_tip( self, ime ):
        '''dohvaca tip iz lokalnog ili sireg djelokruga
        
        pretpostavlja se da je provjereno da je ime deklarirano
            pomocu funkcije self.je_li_deklarirano()
        '''
        if self.nad_djelokrug is not None:
            return self.tablica.get( ime,
                                    self.nad_djelokrug.dohvati_tip( ime ) )
        
        return self.tablica.get( ime, False )
    
    
    def unutar_petlje( self ):
        
        if self.petlja:
            return True
        
        if self.nad_djelokrug is None:
            return False
        
        return self.nad_djelokrug.unutar_petlje()
    
    
    def dohvati_povratni_tip( self ):
        '''dohvaca rekurzivno do globalnog djelokruga povratni tip funkcije'''
        
        if self.povrat is not None:
            return self.povrat
        
        if self.nad_djelokrug is None:
            return None
        
        return self.nad_djelokrug.dohvati_povratni_tip()
    
    
    def __repr__( self ):
        
        ispis = '{\n'
        for ime in self.tablica.keys():
            ispis += ime + ': ' + repr( self.tablica[ime] ) + '\n'
        ispis += '}\n'
        
        return ispis
