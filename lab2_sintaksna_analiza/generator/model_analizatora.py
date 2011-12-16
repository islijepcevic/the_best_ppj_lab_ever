'''model sintaksnog analizatora'''

import sys

from generator.gramatika import Gramatika
from generator.enka import ENKA
from generator.prijelazi import Prijelazi
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
        zapis += repr( 0 )
        
        
        tok = open( datoteka, 'w' )
        tok.write( zapis )
        tok.close()
    
    
    def _stvori_tablice( self ):
        '''najvaznija funkcija koja se poziva iz pri konstrukciji objekta
        
        IVAN
        '''
        
        self._stvori_automat()
        print( 'stvoren automat, ide se na nejednoznacnosti' )
        self._razrijesi_nejednoznacnosti()
        print( 'krece izgradnja tablica' )
        self._izgradi_tablice()
        
    
    
    def _stvori_automat( self ):
        '''stvara enka, nka te na kraju dka i njega sprema pod "svoj" automat
        GOTOVO
        '''
        
        enka = self._kreiraj_enka()
        #nka = enka.kreiraj_nka()
        #dka = nka.kreiraj_dka()
        dka = enka.kreiraj_dka()
        
        self.automat = dka
    
    
    def _kreiraj_enka( self ):
        '''iz gramatike stvara enka
        ovdje ide algoritam sa strane 148
        '''
        
        abeceda = self.gramatika.nezavrsni_znakovi.union(
                                                self.gramatika.zavrsni_znakovi )
        
        pocetno_stanje = LR1Stavka( self.gramatika.pocetni_nezavrsni, [],
                                    self.gramatika.produkcije[-1].desna_strana,
                                    frozenset([ '<<!>>' ]) )
        
        skup_stanja = set([ pocetno_stanje ])   # treba zbog brzine pronalaska stanja u ovom algoritmu
        niz_stanja = [ pocetno_stanje ]     # ovo ce se predavati
        prijelazi = Prijelazi( type( set() ) ) # dict( stanje: dict( znak: set( index-stavke ) ) )
        
        neobradjena_stanja = { 0 }   # index u niz stanja
        
        while( len( neobradjena_stanja ) > 0 ):
            
            trenutno_stanje_index = neobradjena_stanja.pop()
            trenutno_stanje = niz_stanja[ trenutno_stanje_index ]   # tip: LR1Stavka
            
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
            
            index_novog = -1
            if novo_stanje not in skup_stanja:
                skup_stanja.add( novo_stanje )
                index_novog = len( niz_stanja )
                niz_stanja.append( novo_stanje )
                neobradjena_stanja.add( index_novog )
            else:
                index_novog = niz_stanja.index( novo_stanje )
            
            prijelazi.dodaj( trenutno_stanje_index, znak_poslije_tocke, index_novog )
            
            # slucaj iz knjige: 4 c)
            if znak_poslije_tocke in self.gramatika.nezavrsni_znakovi:
                
                # stvori stavku za svaku produkciju iz nezavrsnog znaka q.poslije[0]
                nova_stanja = set([])
                for produkcija in self.gramatika.produkcije:
                    if znak_poslije_tocke == produkcija.lijeva_strana:
                        
                        # T iz knjige, za nastavak LR1Stavke
                        skup_T = self.gramatika.odredi_zapocinje_za_niz(
                                                                nastavak_beta )
                        
                        if self.gramatika.je_li_niz_prazan( nastavak_beta ):
                            skup_T |= ( trenutno_stanje.skup_zapocinje )
                        
                        desni_dio = []
                        if produkcija.desna_strana[0] != '$':
                            desni_dio = produkcija.desna_strana
                        
                        nova_stanja.add( LR1Stavka( znak_poslije_tocke, [],
                                                    desni_dio, skup_T) )
                
                # stavi te sve stavke u prijelaze i stanja (ako nisu u stanjima)
                for novo_stanje in nova_stanja:
                    
                    index_novog = -1
                    if novo_stanje not in skup_stanja:
                        skup_stanja.add( novo_stanje )
                        index_novog = len( niz_stanja )
                        niz_stanja.append( novo_stanje )
                        neobradjena_stanja.add( index_novog )
                    else:
                        index_novog = niz_stanja.index( novo_stanje )
                    
                    prijelazi.dodaj( trenutno_stanje_index, '$', index_novog )
        
        return ENKA( niz_stanja, abeceda, prijelazi )
    
    
    def _razrijesi_nejednoznacnosti( self ):
        
        for skup_stavki in self.automat.stanja:  # stanja automata su u listi
            
            
            # jedno stanje je skup indexa LR1Stavki
            
            # razrijesi pomakni/reduciraj
            sto_zamijeniti = []
            for stavka1_index in skup_stavki:
                
                stavka1 = self.automat.stavke[ stavka1_index ]
                
                if not stavka1 or not stavka1.je_li_potpuna():
                    continue
                
                for stavka2_index in skup_stavki:
                    
                    stavka2 = self.automat.stavke[ stavka2_index ]
                    
                    #ako rjesavam p/r proturjecje izmedju dvije iste stavke, sigurno ce se nepotrebna maknuti znak
                    # prva stavka je potpuna pa mi druga ne treba biti za ovo proturjecje
                    if (not stavka2) or (stavka1 == stavka2) or stavka2.je_li_potpuna():
                        continue
                    
                    # proces razrjesavanja
                    nova_stavka = stavka1.razrijesi_pr( stavka2 )   # vraca novu stavku ili None
                    
                    if nova_stavka is not None:
                        index_nove_stavke = len( self.automat.stavke )
                        self.automat.stavke.append( nova_stavka )
                        
                        # dodaje novu stavku iako vec mozda postoji
                        sto_zamijeniti.append( (self.automat.stanja.index( skup_stavki ), stavka1_index, index_nove_stavke) )
                        
                        # poziv ispisa
                        self._pisi_pr( stavka1, stavka2, nova_stavka, self.automat.stanja.index( skup_stavki ) )
                    
                    # nadam se da je ovdje zbog mutable u self.automatu sve zabiljezeno i promijenjeno
            
            # razrijesi reduciraj/reduciraj
            for stavka1_index in skup_stavki:
                
                stavka1 = self.automat.stavke[ stavka1_index ]
                
                if not stavka1 or not stavka1.je_li_potpuna():
                    continue
                
                for stavka2_index in skup_stavki:
                    
                    stavka2 = self.automat.stavke[ stavka2_index ]
                    
                    if not stavka2 or not stavka2.je_li_potpuna():
                        continue
                    
                    if stavka1 == stavka2:
                        continue
                    
                    skup_za_maknuti = stavka1.skup_zapocinje & stavka2.skup_zapocinje
                    
                    if not skup_za_maknuti:
                        continue
                    
                    produkcija1 = Produkcija( stavka1.lijeva_strana, 
                                    stavka1.desno_prije_tocke + stavka1.desno_poslije_tocke )
                    
                    produkcija2 = Produkcija( stavka2.lijeva_strana, 
                                    stavka2.desno_prije_tocke + stavka2.desno_poslije_tocke )
                    
                    # pronalazi se prva produkcija kako bi se odlucilo r/r proturjecje
                    for prod_gram in self.gramatika.produkcije:
                        
                        if produkcija1 == prod_gram:
                            index_nove_stavke = len( self.automat.stavke )
                            nova_stavka = LR1Stavka( stavka2.lijeva_strana,
                                                    stavka2.desno_prije_tocke,
                                                    stavka2.desno_poslije_tocke,
                                                    stavka2.skup_zapocinje - skup_za_maknuti )
                            self.automat.stavke.append( nova_stavka )
                            
                            sto_zamijeniti.append( (self.automat.stanja.index( skup_stavki ),
                                                    stavka2_index, index_nove_stavke) )
                            
                            self._pisi_rr( stavka2, stavka1, skup_za_maknuti, self.automat.stanja.index( skup_stavki ) )
                            break
                        
                        if produkcija2 == prod_gram:
                            index_nove_stavke = len( self.automat.stavke )
                            nova_stavka = LR1Stavka( stavka1.lijeva_strana,
                                                    stavka1.desno_prije_tocke,
                                                    stavka1.desno_poslije_tocke,
                                                    stavka1.skup_zapocinje - skup_za_maknuti )
                            self.automat.stavke.append( nova_stavka )
                            
                            sto_zamijeniti.append( (self.automat.stanja.index( skup_stavki ),
                                                    stavka1_index, index_nove_stavke) )
                            
                            self._pisi_rr( stavka1, stavka2, skup_za_maknuti, self.automat.stanja.index( skup_stavki ))
                            break
        
        # zamjena stavki u automatu nakon razrjesavanja proturjecja
        # index-stanja; index-stare-stavke, index-nove-razrijesene-stavke
        for istanja, istara, inova in sto_zamijeniti:
            self.automat.stanja[ istanja ].remove( istara )
            self.automat.stanja[ istanja ].add( inova )
    
    
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
            # PO NOVOM SVA SU PRIHVATLJIVA, NEPRIHVATLJIVO IMA INDEX -1
            #if auto.stanja[s] not in auto.prihvatljiva:
                #continue
            
            #print ( s, auto.stanja[s] )
            
            # tablice su otprije prazni nizovi, dodaj elemente prazne dictove
            self.akcija.append(dict())
            self.novo_stanje.append(dict())
            
            # petlja za tablicu akcija
            # iteriranje po LR1Stavkama pojedinog stanja DKA
            for stavka_index in auto.stanja[s]:
                #print( '\t', stavka )
                
                stavka = auto.stavke[ stavka_index ]
                
                # if-uvjet za 'pomakni'
                if not stavka.je_li_potpuna():
                    znak_poslije_tocke = stavka.desno_poslije_tocke[0]
                
                    #print( '\t', znak_poslije_tocke )
                    
                    prijedeno_stanje_index = auto.prijelazi.dohvati( s, znak_poslije_tocke )
                    
                    # dodatni uvjet za pomakni (onaj pravi)
                    if prijedeno_stanje_index != -1 and znak_poslije_tocke in znaci_za_akcije:
                        
                        self.akcija[ s ][ znak_poslije_tocke ] = \
                                    Akcija ('pomakni', prijedeno_stanje_index )
                
                # uvjet za 'prihvati' i 'reduciraj': stavka jest potpuna
                else:
                    
                    # if-uvjet samo za 'prihvati' - bitniji od 'reduciraj'
                    if stavka.lijeva_strana == '<<novi_nezavrsni_znak>>':
                        
                        if stavka.skup_zapocinje == frozenset([ '<<!>>' ]):
                            
                            self.akcija[ s ][ '<<!>>' ] = Akcija( 'prihvati' )
                            
                            continue
                        
                        else:
                            raise GreskaIzgradnjeTablice( 'postoji stavka s novim ' + \
                                'nezavrsnim znakom na lijevoj strani, ' + \
                                'kojoj je skup zapocinje jednak: ' + str( stavka.skup_zapocinje ) )
                    
                    # petlja za 'reduciraj'
                    for znak in stavka.skup_zapocinje:
                        
                        if stavka.desno_prije_tocke == [''] :
                            
                            # da imamo lijepo zapisano, nece slat prazni skup nego onaj epsilon
                            # u obliku znaka '$' bas kao u Ulaznoj!

                            self.akcija[s][ znak ] = Akcija ('reduciraj',
                                                    Produkcija( stavka.lijeva_strana, ['$'] ))
                            
                        else:
                            self.akcija[s][ znak ] = Akcija ('reduciraj',
                            Produkcija( stavka.lijeva_strana, stavka.desno_prije_tocke ))
            
            #petlja za tablicu novo stanje
            for znak in auto.abeceda:
                prijedeno = auto.prijelazi.dohvati( s, znak )
                
                if prijedeno != -1 and znak in self.gramatika.nezavrsni_znakovi:
                    self.novo_stanje[ s ][ znak ] = prijedeno
                
        '''
        print( 'STAVKE DKA' )
        i = 0
        for s in auto.stanja:
            print( i, s )
            i += 1
        print()
        
        print( 'STANJA DKA' )
        i = 0
        for s in auto.stanja:
            print( i, s )
            i += 1
        print()
        
        print( 'PRIJELAZI DKA' )
        #prijelazi_dka.pisi_sve_prijelaze()
        print()
        for i in range( len( auto.stanja ) ):
            for z in auto.abeceda:
                print( i, type(i), z, type(z), auto.prijelazi.dohvati( i, z ) )
        print()
        
        print( 'AKCIJA' )
        #print( self.akcija )
        i = 0
        for s in self.akcija:
            if not s.keys():
                print( i, s )
            for z in s.keys():
                print( i, ',', z, '=', s[z] )
                print()
            i += 1
        print()
        
        print( 'NOVO STANJE') 
        #print( self.novo_stanje )
        i = 0
        for s in self.novo_stanje:
            if not s.keys():
                print( i, s )
            for z in s.keys():
                print( i, z, s[z] )
            i += 1
        print()
        '''
