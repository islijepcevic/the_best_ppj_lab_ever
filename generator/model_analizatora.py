'''model sintaksnog analizatora'''

from generator.gramatika import Gramatika
from generator.enka import ENKA
from generator.lr_1_stavka import LR1Stavka
from generator.akcija import Akcija
from analizator.zajednicki.produkcija import produkcija

class ModelAnalizatora:
    
    def __init__( self, gramatika ):
        
        self.gramatika = gramatika
        self.automat = None
        
        self.akcija = []  # u osnovi ovo je niz (lista)
                            # svaki element liste je rjecnik (dict)
                            # svaki taj dict ima kljuceve koji su zavrsni
                            # znakovi gramatike (string), a vrijednost ce biti objekt
                            # klase Akcija. svaki element niza predstavlja jedan
                            # redak tablice u knjizi;
                            # na pojedinom mjestu u nizu se nalaze akcije za
                            # stanje DKA s istim indexom;
                            # pretpostavlja se da su stanja DKA prirodni brojevi 
                            # (ukljucujuci nulu)
        
        self.novo_stanje = [] # ova tablica je slicna kao akcija, dakle niz
                                # s indexom istim kao za stanje DKA;
                                # clan niza je dict
                                # kljuc dicta je zavrsni znak gramatike (string)
                                # vrijednost dicta je ovdje samo jedan cijeli broj
                                # on oznacava koje se stanje stavlja kao novo stanje
                                # (to je valjda jasno iz predavanja, a i iz samog imena tablice)
        

        
        self._stvori_tablice()
    
    
    def ispisi_tablice( self, datoteka ):
        '''funkcija koja se poziva na kraju iz maina za ispis tablica u neku
        datoteku
        
        ispisuje:
            tablicu akcija
            tablicu novo stanje
            pocetno stanje automata (treba za pocetno stanje stoga)
        IVAN
        '''
        pass
    
    
    def _stvori_tablice( self ):
        '''najvaznija funkcija koja se poziva iz maina
        
        IVAN
        '''
        
        #self._stvori_automat()
        #razrijesi proturjecja - bilo ovdje, bilo u dka
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


        auto = self.automat

        for s in range (len( auto.stanja )):

            self.akcija.append(dict())
            self.novo_stanje.append(dict())


            for i in range (len( auto.stanja[s] )):

                if (( s, auto.stanja[s][i].desno_poslije_tocke[0]) in
                    auto.prijelazi) and (not auto.stanja[s][i].desno_poslije_tocke[0].startswith('<')):
                    kanter += 1

                    self.akcija[s][auto.stanja[s][i].desno_poslije_tocke[0]] = Akcija ('pomakni',
                    auto.prijelazi[(s, auto.stanja[s][i].desno_poslije_tocke[0])])

                if auto.stanja[s][i].je_li_potpuna():
                    
                    if auto.stanja[s][i].lijeva_strana == '<<novi_nezavrsni_znak>>':
                        
                        if auto.stanja[s][i].skup_zapocinje == ['kraj_niza']:

                            self.akcija[s][auto.stanja[s][i].skup_zapocinje[0]] = 'Potvrda()'
      
                        
                            continue
                                           

                    for x in range (len (auto.stanja[s][i].skup_zapocinje)):

                        if auto.stanja[s][i].desno_prije_tocke == [''] :

                            # da imamo lijepo zapisano, nece slat prazni skup nego onaj epsilon
                            # u obliku znaka '$' bas kao u Ulaznoj!

                            self.akcija[s][auto.stanja[s][i].skup_zapocinje[x]] = Akcija ('reduciraj',
                            Produkcija( auto.stanja[s][i].lijeva_strana, '$' ))
                            
                        else:
                            self.akcija[s][auto.stanja[s][i].skup_zapocinje[x]] = Akcija ('reduciraj',
                            Produkcija( auto.stanja[s][i].lijeva_strana, auto.stanja[s][i].desno_prije_tocke ))

                        

            for x in range ( len ( auto.ulazni_znakovi ) ):
                if ((s, auto.ulazni_znakovi[x]) in auto.prijelazi) and auto.ulazni_znakovi[x].startswith('<'):
                    self.novo_stanje[s][auto.ulazni_znakovi[x]] = auto.prijelazi[(s, auto.ulazni_znakovi[x])]

                    
