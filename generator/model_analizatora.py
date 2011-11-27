'''model sintaksnog analizatora'''

from generator.gramatika import Gramatika
from generator.enka import ENKA
from generator.lr_1_stavka import LR1Stavka

class ModelAnalizatora:
    
    def __init__( self, gramatika ):
        
        self.gramatika = gramatika
        self.automat = None
        
        self.akcija = None
        self.novo_stanje = None
    
    
    def ispisi_tablice( self ):
        '''funkcija koja se poziva na kraju iz maina za ispis tablica u neku
        datoteku
        IVAN
        '''
        pass
    
    
    def stvori_tablice( self ):
        '''najvaznija funkcija koja se poziva iz maina
        
        IVAN
        '''
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
