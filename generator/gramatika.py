'''gramatika'''

from analizator.zajednicki.produkcija import Produkcija


class Gramatika:
    
    def __init__( self, nezavrsni_znakovi, zavrsni_znakovi, pocetni_nezavrsni,
                produkcije ):
        
        # tipovi definirani u parseru
        self.nezavrsni_znakovi = nezavrsni_znakovi # skup stringova
        self.zavrsni_znakovi = zavrsni_znakovi # skup stringova
        self.pocetni_nezavrsni = pocetni_nezavrsni # string
        self.produkcije = produkcije    # niz! instanci Produkcije
        
        self.prazni_nezavrsni_znakovi = set([])
        self._zapocinje_znakom = {} # matrica, bit ce dict unutar dicta, svaki
                                    # sa jednakim kljucevima. sadrzavat ce prvo
                                    # ZapocinjeIzravnoZnakom, pa onda
                                    # ZapocinjeZnakom, str 101 - 102
        self._zapocinje = {} # kljuc je JEDAN nezavrsni znak, vrijednost je
                                # skup zavrsnih znakova, str 102, prvi algoritam
        
        # ovo se slijedom dogadja kako bi se gramatika pripremila da daje
        # skup zapocni( niz_znakova )
        
        self._dodaj_novi_pocetni_nezavrsni()
        self._odredi_prazne_znakove()
        self._odredi_zapocinje_izravno_znakom()
        self._odredi_zapocinje_znakom()
        self._odredi_zapocinje_za_nezavrsne()
    
    
    def _dodaj_novi_pocetni_nezavrsni( self ):

        nz = list( self.nezavrsni_znakovi )
        nz.insert(0, '<<novi_nezavrsni_znak>>')
        self.nezavrsni_znakovi = frozenset( nz )
        
        stari_pocetni = self.pocetni_nezavrsni
        self.pocetni_nezavrsni = '<<novi_nezavrsni_znak>>'
        self.produkcije.append( Produkcija('<<novi_nezavrsni_znak>>', [stari_pocetni] ) )

        
    
    def _odredi_prazne_znakove( self ):
        
        # stavi u listu praznih sve lijeve strane epsilon-produkcija
        for i in range (len( self.produkcije )):
            
            if ('$' in self.produkcije[i].desna_strana):
                self.prazni_nezavrsni_znakovi.add(
                    self.produkcije[i].lijeva_strana)
        
        # prosiruj se dok mozes == flood fill
        vrti = True
        while ( vrti ):
            vrti = False
            
            # za svaki znak produkcije
            for i in range (len( self.produkcije )):
                
                # ako je vec u listi praznih - zanemari
                if (self.produkcije[i].lijeva_strana in
                    self.prazni_nezavrsni_znakovi): continue
                
                # 
                for desna_strana in self.produkcije[i].desna_strana:
                    if (desna_strana not in self.prazni_nezavrsni_znakovi):
                        break
                
                # else se izvrsi ako se nije desio break
                else:
                    self.prazni_nezavrsni_znakovi.add(
                        self.produkcije[i].lijeva_strana)
                    vrti = True
        
        self.prazni_nezavrsni_znakovi = frozenset( self.prazni_nezavrsni_znakovi )
    
    
    def _odredi_zapocinje_izravno_znakom( self ):
        

        #stvaranje i inicijalizacija tablice relacije ZapocinjeIzravnoZnakom
        #kasnije se ista "tablica" koristi i za relaciju ZapocinjeZnakom
        #stvara se dict sa svim mogucim kljucevima (2D tablica u knjizi)
        #(nezavrsni + zavrsni) x ( nezavrsni + zavrsni)
        #a vrijednost je boolean
        #self._zapocinje_znakom[znak1, znak2]= int

        # svi kljucevi
        pomocni = self.nezavrsni_znakovi | self.zavrsni_znakovi
        
        # inicijalizacija tablica
        for a in pomocni:
            self._zapocinje_znakom[ a ] = {}
            for b in pomocni:
                self._zapocinje_znakom[ a ][ b ] = False
            
        # funkcija
        
        for produkcija in self.produkcije:
            
            if produkcija.desna_strana[0] == '$': continue
            
            znak_lijevo = produkcija.lijeva_strana
            
            for znak_desno in produkcija.desna_strana:
                
                if znak_desno in self.zavrsni_znakovi:
                    self._zapocinje_znakom[ znak_lijevo ][ znak_desno ] = True
                    break
                elif znak_desno in self.nezavrsni_znakovi:
                    
                    self._zapocinje_znakom[ znak_lijevo ][ znak_desno ] = True
                    
                    if znak_desno not in self.prazni_nezavrsni_znakovi:
                        break
    
    
    def _odredi_zapocinje_znakom( self ):
        
        pomocni = self.nezavrsni_znakovi | self.zavrsni_znakovi
        
        # refleksivno se prosiri
        for a in pomocni:
            self._zapocinje_znakom[ a ][ a ] = True
        
        # tranzitivno se prosiri
        for nezavrsni_znak in self.nezavrsni_znakovi:
            
            neobradjeni = set([])
            
            for znak in pomocni:
                if self._zapocinje_znakom[ nezavrsni_znak ][ znak ]:
                    neobradjeni.add( znak )
            
            neobradjeni.discard( nezavrsni_znak )   # mice ga bio on prisutan
                                                    # ili ne - on je samo za
                                                    # refleksivno okruzenje
            
            # obavi sirenje dok god mozes
            while len( neobradjeni ) > 0:
                trenutni_znak = neobradjeni.pop()
                self._zapocinje_znakom[ nezavrsni_znak ][ trenutni_znak ] = True
                
                for znak in pomocni:
                    # dodaj nove znakove u neobradene ako nisu vec oznaceni
                    if self._zapocinje_znakom[ trenutni_znak ][ znak ] and not \
                        self._zapocinje_znakom[ nezavrsni_znak ][ znak ]:
                        
                        neobradjeni.add( znak )
    
    
    def _odredi_zapocinje_za_nezavrsne( self ):
        

        pomocni = self.nezavrsni_znakovi | self.zavrsni_znakovi
        
        for nz in self.nezavrsni_znakovi:
            temp_skup = set([])
            for zz in self.zavrsni_znakovi:
                if self._zapocinje_znakom[ nz ][ zz ]:
                    temp_skup.add( zz )
            self._zapocinje[ nz ] = temp_skup
    
    
    def odredi_zapocinje_za_niz( self, niz ):
        # ovaj niz treba bit zadan kao produkcija.desna_strana
        # znaci kao niz stringova, a ne 1 string
        
        temp_skup = set([])
        
        if (not niz) or (niz[0] == '$'):
            return set()
            
        else:
            
            for x in range(len( niz )):
                
                if (niz[x] in self.prazni_nezavrsni_znakovi):
                    temp_skup.update( self._zapocinje[niz[x]] )
                    continue
                else: 
                    temp_skup.update( self._zapocinje[niz[x]] )
                    break
                
        return temp_skup
    
    
    def je_li_niz_prazan( self, niz ):
        
        for znak in niz:
            if znak in self.zavrsni_znakovi or \
                (znak not in self.prazni_nezavrsni_znakovi):
                
                break
        else:
            return True
        
        return False
