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

        #print za provjeru
        '''
        for x in range (len(self.produkcije)):
            self.odredi_zapocinje_za_niz(self.produkcije[x].desna_strana)
        '''
    
    
    def _dodaj_novi_pocetni_nezavrsni( self ):

        
        self.nezavrsni_znakovi.insert(0, '<<novi_nezavrsni_znak>>')
        stari_pocetni = self.pocetni_nezavrsni
        self.pocetni_nezavrsni = '<<novi_nezavrsni_znak>>'
        self.produkcije.insert(0, Produkcija('<<novi_nezavrsni_znak>>', stari_pocetni.split() ))

        
    
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
    
    
    def _odredi_zapocinje_izravno_znakom( self ):
        

        #stvaranje i inicijalizacija tablice relacije ZapocinjeIzravnoZnakom
        #kasnije se ista "tablica" koristi i za relaciju ZapocinjeZnakom
        #stvara se dict sa svim mogucim kljucevima (2D tablica u knjizi)
        #(nezavrsni + zavrsni) x ( nezavrsni + zavrsni)
        #a vrijednost je skup od 2 clana sa mogucim vrijednostima 0 ili 1
        #self._zapocinje_znakom[znak1, znak2]=[ZapocinjeIzravnoZnakom, ZapocinjeZnakom]

        # svi kljucevi
        pomocni = self.nezavrsni_znakovi + self.zavrsni_znakovi
        
        # inicijalizacija tablica
        for x in range (len( pomocni )):
            for y in range (len( pomocni )):
                self._zapocinje_znakom[ pomocni[ x ] ][ pomocni[ y ] ] = [0, 0]
            
        # funkcija
        
        for produkcija in self.produkcije:
            
            if produkcija.desna_strana[0] != '$':
                self._zapocinje_znakom[ produkcija ][ 
            
            for znak_desno in produkcija.desna_strana:
                
        
        
        for i in range (len(self.produkcije)):
            for j in range (len( self.produkcije[i].desna_strana )):
                
                if j == 0 and self.produkcije[i].desna_strana[j] != '$':
                    
                    self._zapocinje_znakom[self.produkcije[i].lijeva_strana,
                                        self.produkcije[i].desna_strana[j]] = [1, 1]
                
                if (self.produkcije[i].desna_strana[j] in self.prazni_nezavrsni_znakovi) and (
                    (j + 1) < len(self.produkcije[i].desna_strana)):
                
                    self._zapocinje_znakom[self.produkcije[i].lijeva_strana,
                                        self.produkcije[i].desna_strana[j+1]] = [1, 1]
                else: break



    
    def _odredi_zapocinje_znakom( self ):


        pomocni = self.nezavrsni_znakovi + self.zavrsni_znakovi

        for j in range (len( pomocni )):
            for k in range (len( pomocni )):
                if (pomocni[j] == pomocni [k]):
                    self._zapocinje_znakom[pomocni[j],pomocni[k]][1] = 1

        vrti = True
        while ( vrti ):
            vrti = False
            for a in range (len( pomocni )):
                for b in range (len( pomocni )):
                    for c in range (len( pomocni )):
                        
                        if ((self._zapocinje_znakom[pomocni[a],pomocni[b]][1] == 1) and (
                            self._zapocinje_znakom[pomocni[b],pomocni[c]][1] == 1)):
                            if self._zapocinje_znakom[pomocni[a],pomocni[c]][1] == 0:
                                self._zapocinje_znakom[pomocni[a],pomocni[c]][1] = 1
                                vrti = True
                        
                                                    
                    
        #print za provjeru
        '''
        for x in range (len(pomocni)):
            for y in range (len(pomocni)):
                if self._zapocinje_znakom[pomocni[x],
                                       pomocni[y]] != [0,0]:
                    print(pomocni[x]+' , '+ pomocni[y]+ ' '+str(self._zapocinje_znakom[
                        pomocni[x], pomocni[y]]))
        '''


    
    def _odredi_zapocinje_za_nezavrsne( self ):
        

        pomocni = self.nezavrsni_znakovi + self.zavrsni_znakovi
        
        for x in range (len( pomocni )):
            temp_skup = []
            for y in range (len( pomocni )):
                if self._zapocinje_znakom[pomocni[x], pomocni[y]][1] == 1 and (
                    pomocni[y] in self.zavrsni_znakovi):
                    temp_skup.append(pomocni[y])
            self._zapocinje[pomocni[x]] = temp_skup

            
        #print za provjeru
        '''
        for x in range (len(pomocni)):
           print(pomocni[x] +': '+ str(self._zapocinje[pomocni[x]]))
        '''
            
    
    
    def odredi_zapocinje_za_niz( self, niz ):


        # ovaj niz treba bit zadan kao produkcija.desna_strana
        # znaci kao niz stringova, a ne 1 string
        
        temp_skup = []
        if niz[0] == '$':
            self._zapocinje[str(niz)] = set()
            
        else:
            
            
            for x in range(len( niz )):
                
                if (niz[x] in self.prazni_nezavrsni_znakovi):
                    temp_skup.extend(self._zapocinje[niz[x]])
                    continue
                else: 
                    temp_skup.extend(self._zapocinje[niz[x]])
                    break
                
        self._zapocinje[str(niz)] = set(temp_skup)
        
        #print ('Zapocinje'+ str(niz)+ str(self._zapocinje[str(niz)]))
                                 

    
                



