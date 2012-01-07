'''glavni kod i klasa semantickog analizatora'''

from analizator.nezavrsni_znak import NezavrsniZnak
from analizator.leksicka_jedinka import LeksickaJedinka

from analizator.djelokrug import Djelokrug
from analizator.tipovi_podataka import JednostavniTip, TipFunkcija, TipNiz

class SemantickiAnalizator:
    
    def __init__( self, generativno_stablo, tok_za_ispis, tok_za_greske ):
        
        self.generativno_stablo = generativno_stablo
        
        self.tok_za_ispis = tok_za_ispis
        self.tok_za_greske = tok_za_greske
        
        # popis funkcija s definicijom, k: ime, v: tip
        self.definirane_funkcije = {}
        
        # za provjere nakon obilaska stabla, k: ime, v: tip
        self.funkcije_bez_definicije = {}
        self.mainPostoji = False
    
    
    def analiziraj( self ):
        
        # inicijaliziraj globalni djelokrug
        globalni_djelokrug = Djelokrug( None )
        
        # ako je korijen pocetni nezavrsni:
            # pozovi self.prijevodna_jedinica()
        if type( self.generativno_stablo ) == NezavrsniZnak and \
            self.generativno_stablo.nezavrsni_znak == '<prijevodna_jedinica>':
            
            if not self.prijevodna_jedinica( self.generativno_stablo,
                                            globalni_djelokrug ):
                return False
        
        if not self.mainPostoji:
            self.tok_za_ispis.write( 'main' )
            return False
        
        if len( self.funkcije_bez_definicije.keys() ) > 0:
            self.tok_za_ispis.write( 'funkcija' )
            return False
        
        return True
    
    
    def ispisi_produkciju( self, cvor ):
        
        ispis = cvor.nezavrsni_znak + ' ::='
        
        for dijete in cvor.djeca:
            
            if type( dijete ) == NezavrsniZnak:
                ispis += ' ' + dijete.nezavrsni_znak
            
            else:
                ispis += ' ' + dijete.uniformni_znak
                ispis += '(' + dijete.redak
                ispis += ',' + dijete.leksicka_jedinka + ')'
        
        ispis += '\n'
        
        self.tok_za_ispis.write( ispis )
        return
    
    
    '''
    povratna vrijednost svih funkcija rekurzivnog spusta:
        True ako nema greske
        False ako ima greske
    '''
    '''
    za izvedena svojstva:
        funkcija se poziva sa dictom koji ce primiti svojstva
    '''
    
    
    ############################################################################
    ############################### IZRAZI #####################################
    ############################################################################
    
    
    def ime_tipa( self, cvor, izvedena_svojstva = {} ):
        
        svojstva_spec_tipa = {}
        tip = None
        
        if len( cvor.djeca ) == 1:
            
            if not self.specifikator_tipa( cvor.djeca[0], svojstva_spec_tipa ):
                return False
            
            tip = svojstva_spec_tipa['tip']
        
        else:
            
            if not self.specifikator_tipa( cvor.djeca[1], svojstva_spec_tipa ):
                return False
            
            if svojstva_spec_tipa['tip'].je_li_void():
                self.ispisi_produkciju( cvor )
                return False
            
            tip = JednostavniTip( svojstva_spec_tipa['tip'], True )
        
        izvedena_svojstva['tip'] = tip
        return True
    
    
    def specifikator_tipa( self, cvor, izvedena_svojstva = {} ):
        
        tip = None
        
        if cvor.djeca[0].uniformni_znak == 'KR_CHAR':
            tip = 'char'
        
        elif cvor.djeca[0].uniformni_znak == 'KR_INT':
            tip = 'int'
        
        else: # 'KR_VOID'
            tip = 'void'
        
        izvedena_svojstva['tip'] = JednostavniTip( tip )
        return True
    
    
    def izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        pass
    
    
    ############################################################################
    ###################### NAREDBENA STRUKTURA PROGRAMA ########################
    ############################################################################
    
    
    def slozena_naredba( self, cvor, djelokrug, tip_funkcije = None,
                        imena_parametara = None ):
        
        cvor_naredbe = cvor.djeca[1]
        lokalni_djelokrug = Djelokrug( djelokrug )
        
        # prebacivanje parametara funkcije u lokalni djelokrug
        if tip_funkcije is not None and not tip_funkcije.je_li_domena_void():
            
            for tip, ime in zip( tip_funkcije.domena, imena_parametara ):
                lokalni_djelokrug.dodaj( ime, tip )
        
        if cvor.djeca[1].nezavrsni_znak == '<lista_deklaracija>':
            
            cvor_naredbe = cvor.djeca[2]
            
            if not self.lista_deklaracija( cvor.djeca[1], lokalni_djelokrug ):
                return False
        
        return self.lista_naredbi( cvor_naredbe, lokalni_djelokrug )
    
    
    def lista_naredbi( self, cvor, djelokrug ):
        
        cvor_naredba = cvor.djeca[0]
        
        if cvor.djeca[0].nezavrsni_znak == '<lista_naredbi>':
            cvor_naredba = cvor.djeca[1]
            
            if not self.lista_naredbi( cvor.djeca[0], djelokrug ):
                return False
        
        return self.naredba( cvor_naredba, djelokrug )
    
    
    def naredba( self, cvor, djelokrug ):
        
        cvor_znak = cvor.djeca[0].nezavrsni_znak
        
        if cvor_znak == '<slozena_naredba>':
            return self.slozena_naredba( cvor.djeca[0], djelokrug )
            
        elif cvor_znak == '<izraz_naredba>':
            return self.izraz_naredba( cvor.djeca[0], djelokrug )
            
        elif cvor_znak == '<naredba_grananja>':
            return self.naredba_grananja( cvor.djeca[0], djelokrug )
            
        elif cvor_znak == '<naredba_petlje>':
            return self.naredba_petlje( cvor.djeca[0], djelokrug )
        
        # zadnji slucaj: cvor_znak == '<naredba_skoka>'
        return self.naredba_skoka( cvor.djeca[0], djelokrug )
    
    
    def izraz_naredba( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = 'int'
        
        if len( cvor.djeca ) > 1:
            
            svojstva_izraz = {}
            if not self.izraz( cvor.djeca[0], djelokrug, svojstva_izraz ):
                return False
            
            tip = svojstva_izraz['tip']
        
        izvedena_svojstva['tip'] = tip
        return True
    
    
    def naredba_grananja( self, cvor, djelokrug ):
        pass
    
    
    def naredba_petlje( self, cvor, djelokrug ):
        pass
    
    
    def naredba_skoka( self, cvor, djelokrug ):
        pass
    
    
    def prijevodna_jedinica( self, cvor, djelokrug ):
        '''pocetni nezavrsni znak gramatike'''
        
        povratak = True
        
        if cvor.djeca[0].nezavrsni_znak == '<vanjska_deklaracija>':
            
            povratak = self.vanjska_deklaracija( cvor.djeca[0], djelokrug )
        
        else:
            
            povratak = self.prijevodna_jedinica( cvor.djeca[0], djelokrug )
            povratak = self.vanjska_deklaracija( cvor.djeca[1], djelokrug )
            
        return povratak
    
    
    def vanjska_deklaracija( self, cvor, djelokrug ):
        
        povratak = True
        if cvor.djeca[0].nezavrsni_znak == '<definicija_funkcije>':
            
            povratak = self.definicija_funkcije( cvor.djeca[0], djelokrug )
        
        else:   # nezavrsni_znak == '<deklaracija>'
            
            povratak = self.deklaracija( cvor.djeca[0], djelokrug )
        
        return povratak
    
    
    ############################################################################
    ####################### DEKLARACIJE I DEFINICIJE ###########################
    ############################################################################
    
    
    def definicija_funkcije( self, cvor, djelokrug ):
        
        svojstva_ime_tipa = {}
        povratak = self.ime_tipa( cvor.djeca[0], svojstva_ime_tipa )
        
        if not povratak:
            return False
        
        # provjera je li const (ne smije biti)
        if svojstva_ime_tipa['tip'].je_li_const():
            self.ispisi_produkciju( cvor )
            return False
        
        ime = cvor.djeca[1].leksicka_jedinka
        
        # postoji li vec definicija funkcije funkcije s ovim imenom
        if ime in self.definirane_funkcije.keys():
            self.ispisi_produkciju( cvor )
            return False
        
        svojstva_parametri = { 'tipovi': JednostavniTip('void') }
        
        # ako ima parametara
        if type( cvor.djeca[3] ) == NezavrsniZnak:
            
            svojstva_parametri = {}
            povratak = self.lista_parametara( cvor.djeca[3],
                                            svojstva_parametri )
            
            if not povratak:
                return False
        
        tip_funkcije = TipFunkcija( svojstva_parametri['tipovi'],
                                    svojstva_ime_tipa['tip'] )
        
        # main funkcija
        if ime == 'main' and tip_funkcije == \
            TipFunkcija( JednostavniTip('void'), JednostavniTip('int') ):
            
            self.mainPostoji = True
        
        # postojanje deklaracije ove funkcije u globalnom djelokrugu
        if not djelokrug.provjeri_funkciju( ime, tip_funkcije ):
            self.ispisi_produkciju( cvor )
            return False
        
        # makni funkciju iz popisa nedefiniranih funkcija
        if ime in self.funkcije_bez_definicije.keys() and \
            tip_funkcije == self.funkcije_bez_definicije[ ime ]:
            
            del self.funkcije_bez_definicije[ ime ]
        
        #zabiljezi definiciju i deklaraciju
        self.definirane_funkcije[ ime ] = tip_funkcije
        djelokrug.dodaj( ime, tip_funkcije )
        
        if type( svojstva_parametri['tipovi'] ) == JednostavniTip and \
            svojstva_parametri['tipovi'].je_li_void():
            
            return self.slozena_naredba( cvor.djeca[5], djelokrug,
                                        tip_funkcije )
        else:
            return self.slozena_naredba( cvor.djeca[5], djelokrug, tip_funkcije,
                                        svojstva_parametri['imena'] )
    
    
    def lista_parametara( self, cvor, izvedena_svojstva = {} ):
        
        tipovi = []
        imena = []
        
        cvor_deklaracija = cvor.djeca[0]
        
        if cvor.djeca[0].nezavrsni_znak == '<lista_parametara>':
            
            cvor_deklaracija = cvor.djeca[2]
            
            svojstva_lista = {}
            if not self.lista_parametara( cvor.djeca[0], svojstva_lista ):
                return False
            
            tipovi = svojstva_lista['tipovi']
            imena = svojstva_lista['imena']
        
        svojstva_deklaracija = {}
        if not self.deklaracija_parametra( cvor_deklaracija,
                                            svojstva_deklaracija ):
            return False
        
        if cvor.djeca[0].nezavrsni_znak == '<lista_parametara>' and \
            svojstva_deklaracija['ime'] in svojstva_lista['imena']:
            
            self.ispisi_produkciju( cvor )
            return False
        
        tipovi.append( svojstva_deklaracija['tip'] )
        imena.append( svojstva_deklaracija['ime'] )
        
        izvedena_svojstva['tipovi'] = tipovi
        izvedena_svojstva['imena'] = imena
        
        return True
    
    
    def deklaracija_parametra( self, cvor, izvedena_svojstva = {} ):
        
        svojstva_tip = {}
        if not self.ime_tipa( cvor.djeca[0], svojstva_tip ):
            return False
        
        tip = svojstva_tip['tip']
        
        if tip.je_li_void():
            self.ispisi_produkciju( cvor )
            return False
        
        ime = cvor.djeca[1].leksicka_jedinka
        
        if len( cvor.djeca ) > 2:
            tip = TipNiz( tip )
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['ime'] = ime
        
        return True
    
    
    def lista_deklaracija( self, cvor, djelokrug ):
        pass
    
    
    def deklaracija( self, cvor, djelokrug ):
        pass
