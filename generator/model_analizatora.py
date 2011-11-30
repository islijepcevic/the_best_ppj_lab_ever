'''model sintaksnog analizatora'''

from generator.gramatika import Gramatika
from generator.enka import ENKA
from generator.lr_1_stavka import LR1Stavka
from generator.akcija import Akcija

class ModelAnalizatora:
    
    def __init__( self, gramatika ):
        
        self.gramatika = gramatika
        self.automat = None
        
        self.akcija = None  # u osnovi ovo je niz (lista)
                            # svaki element liste je rjecnik (dict)
                            # svaki taj dict ima kljuceve koji su zavrsni
                            # znakovi gramatike (string), a vrijednost ce biti objekt
                            # klase Akcija. svaki element niza predstavlja jedan
                            # redak tablice u knjizi;
                            # na pojedinom mjestu u nizu se nalaze akcije za
                            # stanje DKA s istim indexom;
                            # pretpostavlja se da su stanja DKA prirodni brojevi 
                            # (ukljucujuci nulu)
        
        self.novo_stanje = None # ova tablica je slicna kao akcija, dakle niz
                                # s indexom istim kao za stanje DKA;
                                # clan niza je dict
                                # kljuc dicta je zavrsni znak gramatike (string)
                                # vrijednost dicta je ovdje samo jedan cijeli broj
                                # on oznacava koje se stanje stavlja kao novo stanje
                                # (to je valjda jasno iz predavanja, a i iz samog imena tablice)
        
        # Gorane, ne trebas za svaki redak i stupac tablica dodavati akciju
        # ako je neki redak potpuno prazan, neka ostane prazan dicta
        # ako u nekom retku za neki stupac nema akcije, neka ne postoji taj kljuc
        # u dict. tako cemo lakse valjda i debugirati kasnije jer ce se zbog neceg 
        # program skrsiti ako se nesto krivo izvelo (a u slucaju da svim nepotrebnima
        # stavis npr None za vrijednost, mozda bi se nesto viska izvelo i teze bi 
        # pronasli gresku) - ovo su samo pretpostavke, ali radimo tako
        
        self._stvori_tablice()
    
    
    def ispisi_tablice( self, datoteka ):
        '''funkcija koja se poziva na kraju iz maina za ispis tablica u neku
        datoteku
        IVAN
        '''
        pass
    
    
    def _stvori_tablice( self ):
        '''najvaznija funkcija koja se poziva iz maina
        
        IVAN
        '''
        
        #self._stvori_automat()
        #self._izgradi_tablice()
        pass
    
    
    def _kreiraj_enka( self ):
        '''iz gramatike stvara enka
        ovdje ide algoritam sa strane 148
        SARA
        '''
        
        '''napomena: imam pseudokod ovoga kako bi trebalo izgledati
        vjerojatno cu ga staviti tu, ili cu sam ovo napisati
        '''
        pass
    
    
    def _stvori_automat( self ):
        '''stvara enka, nka te na kraju dka i njega sprema pod "svoj" automat
        GOTOVO
        '''
        
        enka = self._kreiraj_enka()
        nka = enka.kreiraj_nka()
        dka = nka.kreiraj_dka()
        
        self.automat = dka
    
    
    def _izgradi_tablice( self ):
        '''izgradjuje tablice Akcija i NovoStanje
        tablice jos nisu definirane kakvog ce tipa biti
        to jos i ovisi o tome kako ce DKA tocno izgledati
        knjiga str 150 - 151
        
        GORAN
        '''
        
        '''napomena: pazi na proturjecja, uputa-za-labos 3.1.6'''
        pass
