'''model sintaksnog analizatora'''

import sys

from generator.gramatika import Gramatika
from generator.enka import ENKA
from generator.lr_1_stavka import LR1Stavka
from analizator.zajednicki.akcija import Akcija
from analizator.zajednicki.produkcija import Produkcija
from analizator.zajednicki.greske import GreskaIzgradnjeTablice

class ModelAnalizatora:
    
    def __init__( self, gramatika, tok_za_pogreske = sys.stderr ):
        
        self.tok_za_pogreske = tok_za_pogreske
        
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
                                # kljuc dicta je nezavrsni znak gramatike (string)
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
        
        zapis = repr( self.akcija ) + '\n'
        zapis += repr( self.novo_stanje ) + '\n'
        zapis += repr( self.automat.pocetno_stanje )
        
        
        tok = open( datoteka, 'w' )
        tok.write( zapis )
        tok.close()
    
    
    def _stvori_tablice( self ):
        '''najvaznija funkcija koja se poziva iz maina
        
        IVAN
        '''
        
        self._stvori_automat()
        self._razrijesi_nejednoznacnosti()
        self._izgradi_tablice()
        
    
    
    def _kreiraj_enka( self ):
        '''iz gramatike stvara enka
        ovdje ide algoritam sa strane 148
        '''
        
        abeceda = self.gramatika.nezavrsni_znakovi.union( 
                            self.gramatika.zavrsni_znakovi )
        
        pocetno_stanje = LR1Stavka( self.gramatika.pocetni_nezavrsni, [],
                                    self.gramatika.produkcije[-1].desna_strana,
                                    frozenset([ '<<!>>' ]) )
        
        skup_stanja = set([ pocetno_stanje ])
        prijelazi = {}  # rjecnik: kljuc = par (LR1Stavka, string)
                        # vrijednost = skup LR1Stavki
        
        neobradjena_stanja = skup_stanja.copy()
        
        while( len( neobradjena_stanja ) > 0 ):
            
            trenutno_stanje = neobradjena_stanja.pop()  # tip: LR1Stavka
            
            # potpuna stavka
            if trenutno_stanje.desno_poslije_tocke == "":
                continue
            
            # slucaj iz knjige: 4 b)
            
            if trenutno_stanje.je_li_potpuna():
                continue
            
            znak_poslije_tocke = trenutno_stanje.desno_poslije_tocke[0]
            
            nastavak_beta = []
            if len( trenutno_stanje.desno_poslije_tocke ) > 1:
                nastavak_beta = trenutno_stanje.desno_poslije_tocke[1:]
            
            novo_stanje = LR1Stavka( trenutno_stanje.lijeva_strana,
                                    trenutno_stanje.desno_prije_tocke + [znak_poslije_tocke ],
                                    nastavak_beta,
                                    trenutno_stanje.skup_zapocinje )
            
            if novo_stanje not in skup_stanja:
                skup_stanja.add( novo_stanje )
                neobradjena_stanja.add( novo_stanje )
            
            kljuc = (trenutno_stanje, znak_poslije_tocke)
            if kljuc in prijelazi:
                prijelazi[ kljuc ] |= frozenset([ novo_stanje ])
            else:
                prijelazi[ kljuc ] = frozenset([ novo_stanje ])
            
            # slucaj iz knjige: 4 c)
            if znak_poslije_tocke in self.gramatika.nezavrsni_znakovi:
                
                # stvori stavku za svaku produkciju iz nezavrsnog znaka q.poslije[0]
                nova_stanja = set([])
                for produkcija in self.gramatika.produkcije:
                    if znak_poslije_tocke == produkcija.lijeva_strana:
                        
                        skup_T = self.gramatika.odredi_zapocinje_za_niz(
                                                                nastavak_beta )
                        
                        if self.gramatika.je_li_niz_prazan( nastavak_beta ):
                            skup_T |= ( trenutno_stanje.skup_zapocinje )
                        
                        desni_dio = ['']
                        if produkcija.desna_strana[0] != '$':
                            desni_dio = produkcija.desna_strana
                        
                        nova_stanja.add( LR1Stavka( znak_poslije_tocke, [],
                                                    desni_dio, skup_T) )
                
                # stavi te sve stavke u prijelaze i stanja (ako nisu u stanjima)
                for novo_stanje in nova_stanja:
                    
                    if novo_stanje not in skup_stanja:
                        skup_stanja.add( novo_stanje )
                        neobradjena_stanja.add( novo_stanje )
                    
                    kljuc = (trenutno_stanje, '$')
                    if kljuc in prijelazi:
                        prijelazi[ kljuc ] |= frozenset([ novo_stanje ])
                    else:
                        prijelazi[ kljuc ] = frozenset([ novo_stanje ])
        
        
        return ENKA( skup_stanja, abeceda, pocetno_stanje, skup_stanja.copy(),
                    prijelazi )
    
    
    def _stvori_automat( self ):
        '''stvara enka, nka te na kraju dka i njega sprema pod "svoj" automat
        GOTOVO
        '''
        
        enka = self._kreiraj_enka()
        nka = enka.kreiraj_nka()
        dka = nka.kreiraj_dka()
        
        self.automat = dka
    
    
    def _razrijesi_nejednoznacnosti( self ):
        #print( type(self.automat.stanja), self.automat.stanja )
        for stanje in self.automat.stanja:  # stanja automata su u listi
            
            # jedno stanje je skup LR1Stavki
            
            #print( type(stanje), stanje )
            # razrijesi pomakni/reduciraj
            #for i in range( len( stanje ) ):
            for stavka1 in stanje:
                #print( type(stavka1), stavka1 )
                if not stavka1.je_li_potpuna():
                    continue
                
                for stavka2 in stanje:
                    
                    if stavka1 == stavka2:
                        continue
                    
                    #stavka1 = stanje[i]
                    #stavka2 = stanje[j]
                    
                    ret = stavka1.razrijesi_pr( stavka2 )
                    
                    if ret:
                        self._pisi_pr( stavka1, stavka2, ret, self,automat.stanja.index( stanje ) )
                    
                    #stanje[i] = stavka1
                    # nadam se da je ovdje zbog mutable u self.automatu sve zabiljezeno i promijenjeno
            
            # razrijesi reduciraj/reduciraj
            for stavka1 in stanje:
                
                if not stavka1.je_li_potpuna():
                    continue
                
                #for j in range( i + 1, len( stanje ) ):
                for stavka2 in stanje:
                    
                    if not stavka2.je_li_potpuna():
                        continue
                    
                    #stavka1 = stanje[i]
                    #stavka2 = stanje[j]
                    
                    skup_za_maknuti = stavka1.skup_zapocinje & stavka2.skup_zapocinje
                    
                    if not skup_za_maknuti:
                        continue
                    
                    produkcija1 = Produkcija( stavka1.lijeva_strana, 
                                    stavka1.desno_prije_tocke + stavka1.desno_poslije_tocke )
                    
                    produkcija2 = Produkcija( stavka2.lijeva_strana, 
                                    stavka2.desno_prije_tocke + stavka2.desno_poslije_tocke )
                    
                    for prod_gram in self.gramatika.produkcije:
                        
                        if produkcija1 == prod_gram:
                            stavka2.skup_zapocinje -= skup_za_maknuti
                            self._pisi_rr( stavka2, stavka1, skup_za_maknuti, self.automat.stanja.index( stanje ) )
                            break
                        
                        if produkcija2 == prod_gram:
                            stavka1.skup_zapocinje -= skup_za_maknuti
                            self._pisi_rr( stavka1, stavka2, skup_za_maknuti, self.automat.stanja.index( stanje ))
                            break
                    
                    #stanje[i] = stavka1
                    #stanje[j] = stavka2
    
    
    def _pisi_pr( self, stavka, druga, maknuto, stanje ):
        
        ispis = 'u stanju ' + str( stanje ) + '\n'
        ispis += 'iz stavke ' + str( stavka) + '\n'
        ispis += 'maknuti su znaci: ' + str(maknuto) + '\n'
        ispis += 'zbog proturjecja pomakni/reduciraj sa stavkom ' + str(druga) + '\n'
        ispis += '\n'
        
        self.tok_za_pogreske.write( ispis )
    
    
    def _pisi_rr( self, stavka, druga, skup_za_maknuti, stanje ):
        
        ispis = 'u stanju ' + str(stanje) + '\n'
        ispis += 'iz stavke ' + str(stavka) + '\n'
        ispis += 'maknuti su znaci: ' + str( skup_za_maknuti ) + '\n'
        ispis += 'zbog proturjecja reduciraj/reduciraj sa stavkom ' + str( druga ) + '\n'
        ispis += '\n'
        
        self.tok_za_pogreske.write( ispis )
    
    
    def _izgradi_tablice( self ):


        auto = self.automat
        znaci_za_akcije = self.gramatika.zavrsni_znakovi | set([ '<<!>>' ])

        for s in range (len( auto.stanja )):
            
            # zanemari neprihvatljiva stanja
            if auto.stanja[s] not in auto.prihvatljiva:
                continue
            
            # tablice su otprije prazni nizovi, dodaj element prazni dict
            self.akcija.append(dict())
            self.novo_stanje.append(dict())

            # petlja za tablicu akcija
            # iteriranje po LR1Stavkama pojedinog stanja DKA
            for stavka in auto.stanja[s]:
                
                if stavka.je_li_potpuna():
                    continue
                znak_poslije_tocke = stavka.desno_poslije_tocke[0]
                
                # if-uvjet za 'pomakni'
                if ( ( s, znak_poslije_tocke) in auto.prijelazi ) \
                    and (znak_poslije_tocke in znaci_za_akcije ):
                    
                    self.akcija[s][ znak_poslije_tocke ] = \
                        Akcija ('pomakni', auto.prijelazi[ (s, znak_poslije_tocke) ] )
                
                # if-uvjet za 'prihvati' i 'reduciraj'
                if stavka.je_li_potpuna():
                    
                    # if-uvjet samo za 'prihvati' - bitniji od 'reduciraj'
                    if stavka.lijeva_strana == '<<novi_nezavrsni_znak>>':
                        
                        if stavka.skup_zapocinje == frozenset([ '<<!>>' ]):
                            
                            self.akcija[s][ znak_poslije_tocke ] = Akcija( 'prihvati' )
                            
                            continue
                        
                        else:
                            raise GreskaIzgradnjeTablice( 'postoji stavka s novim nezavrsnim znakom, ' + \
                                'kojoj je skup zapocinje jednak: ' + str( stavka.skup_zapocinje ) )
                    
                    # petlja za 'reduciraj'
                    for x in range (len (auto.stanja[s][i].skup_zapocinje)):
                        
                        if stavka.desno_prije_tocke == [''] :
                            
                            # da imamo lijepo zapisano, nece slat prazni skup nego onaj epsilon
                            # u obliku znaka '$' bas kao u Ulaznoj!

                            self.akcija[s][ stavka.skup_zapocinje[x] ] = Akcija ('reduciraj',
                                                    Produkcija( stavka.lijeva_strana, ['$'] ))
                            
                        else:
                            self.akcija[s][ stavka.skup_zapocinje[x] ] = Akcija ('reduciraj',
                            Produkcija( stavka.lijeva_strana, stavka.desno_prije_tocke ))
                        
            #petlja za tablicu novo stanje
            for znak in auto.ulazni_znakovi:
                if ((s, znak) in auto.prijelazi) and \
                    znak in self.gramatika.nezavrsni_znakovi:
                    
                    self.novo_stanje[s][ znak ] = auto.prijelazi[(s, znak )]
