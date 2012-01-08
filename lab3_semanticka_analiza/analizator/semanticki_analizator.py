'''glavni kod i klasa semantickog analizatora'''

from curses import ascii

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
        
        # za provjere nakon obilaska stabla, k: ime, v: set( tip )
        self.funkcije_bez_definicije = {}
        self.mainPostoji = False
    
    
    def analiziraj( self ):
        
        # inicijaliziraj globalni djelokrug
        globalni_djelokrug = Djelokrug()
        
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
    
    
    def pisi( self, predmet ):
        
        self.tok_za_greske.write( repr( predmet ) + '\n' )
    
    
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
    
    
    def primarni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        prva_jedinka = cvor.djeca[0]
        
        if prva_jedinka.uniformni_znak == 'IDN':
            
            ime = prva_jedinka.leksicka_jedinka
            
            if not djelokrug.je_li_deklarirano( ime ):
                self.ispisi_produkciju( cvor )
                return False
            
            tip = djelokrug.dohvati_tip( ime )
            l_izraz = tip.je_li_l_izraz()
        
        elif prva_jedinka.uniformni_znak == 'BROJ':
            
            vrijednost = int( prva_jedinka.leksicka_jedinka )
            
            if vrijednost < (- 2 ** 31 ) or vrijednost > ( 2 ** 31 - 1 ):
                self.tok_za_greske.write( 'sto pise: ' + \
                                            prva_jedinka.leksicka_jedinka + \
                                            '\n' )
                self.tok_za_greske.write( 'sto se dobilo: ' + \
                                            str( vrijednost ) + '\n' )
                self.ispisi_produkciju( cvor )
                return False
            
            tip = JednostavniTip( 'int' )
            l_izraz = False
        
        elif prva_jedinka.uniformni_znak == 'ZNAK':
            
            znak = prva_jedinka.leksicka_jedinka
            
            if len( znak ) > 3:
                prefiksirani = znak[2]
                
                dozvoljeni = { 't', 'n', '0', '\'', '"', '\\' }
                
                if prefiksirani not in dozvoljeni:
                    self.ispisi_produkciju( cvor )
                    return False
            
            if not ascii.isprint( znak[1] ):
                self.ispisi_produkciju( cvor )
                return False
            
            tip = JednostavniTip( 'char' )
            l_izraz = False
        
        elif prva_jedinka.uniformni_znak == 'NIZ_ZNAKOVA':
            
            niz = prva_jedinka.leksicka_jedinka
            
            prefiksirano = False
            
            specijalni = { 't': '\t', 'n': '\n', '\'': '\'', '"': '\"', \
                            '\\': '\\' }
            
            for znak in niz[1:-1]:
                
                if prefiksirano:
                    prefiksirano = False
                    
                    prefiksirani_znak = specijalni.get( znak )
                    
                    if prefiksirani_znak is None:
                        self.ispisi_produkciju( cvor )
                        return False
                
                else:
                    
                    if znak == '\\':
                        prefiksirano = True
                    
                    else:
                        if not ascii.isprint( znak ):
                            self.ispisi_produkciju( cvor )
                            return False
            
            if prefiksirano:
                self.ispisi_produkciju( cvor )
                return False
            
            tip = TipNiz( JednostavniTip( 'char', True ) )
            l_izraz = False
        
        else:   # (<izraz>)
            
            svojstva_izraz = {}
            if not self.izraz( cvor.djeca[1], djelokrug, svojstva_izraz ):
                return False
            
            tip = svojstva_izraz['tip']
            l_izraz = svojstva_izraz['l-izraz']
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def postfiks_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        self.pisi( 'postfiks' )
        # primarni_izraz
        if len( cvor.djeca ) == 1:
            
            svojstva_primarni = {}
            if not self.primarni_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_primarni ):
                return False
            
            tip = svojstva_primarni['tip']
            l_izraz = svojstva_primarni['l-izraz']
        
        else:
            
            svojstva_postfiks = {}
            if not self.postfiks_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_postfiks ):
                return False
        
            # OP_INC / OP_DEC
            if len( cvor.djeca ) == 2:
                
                tip = JednostavniTip( 'int' )
                
                if not svojstva_postfiks['l-izraz'] or \
                    not svojstva_postfiks['tip'].je_li_svodivo( tip ):
                    
                    self.ispisi_produkciju( cvor )
                    return False
                
                l_izraz = False
            
            # funkcija s void domenom
            elif len( cvor.djeca ) == 3:
                
                if type( svojstva_postfiks['tip'] ) != TipFunkcija or \
                    not svojstva_postfiks['tip'].domena.je_li_void():
                    
                    self.ispisi_produkciju( cvor )
                    return False
                
                tip = svojstva_postfiks['tip'].kodomena
                l_izraz = False
            
            # funkcija s listom parametara
            elif cvor.djeca[1].uniformni_znak == 'L_ZAGRADA':
                
                svojstva_argumenti = {}
                if not self.lista_argumenata( cvor.djeca[2], djelokrug,
                                            svojstva_argumenti ):
                    return False
                
                if type( svojstva_postfiks['tip'] ) != TipFunkcija or \
                    svojstva_postfiks['tip'].domena.je_li_void():
                    
                    self.ispisi_produkciju( cvor )
                    return False
                
                tipovi_parametara = svojstva_postfiks['tip'].domena
                tipovi_argumenata = svojstva_argumenti['tipovi']
                
                if len( tipovi_parametara ) != len( tipovi_argumenata ):
                    self.ispisi_produkciju( cvor )
                    return False
                
                for tip_parametra, tip_argumenta in zip( tipovi_parametara,
                                                        tipovi_argumenata):
                    
                    if not tip_argumenta.je_li_svodivo( tip_parametra ):
                        self.ispisi_produkciju( cvor )
                        return False
                
                tip = svojstva_postfiks['tip'].kodomena
                l_izraz = False
            
            # indeksiranje nizova
            else:
                
                if type( svojstva_postfiks['tip'] ) != TipNiz:
                    self.ispisi_produkciju( cvor )
                    return False
                
                svojstva_izraz = {}
                if not self.izraz( cvor.djeca[2], djelokrug, svojstva_izraz ):
                    return False
                
                if not svojstva_izraz.je_li_svodivo( JednostavniTip( 'int' ) ):
                    self.ispisi_produkciju( cvor )
                    return False
                
                # dohvati jednostavni tip niza
                tip = svojstva_postfiks['tip'].tip
                l_izraz = not tip.je_li_const
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def lista_argumenata( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tipovi = []
        
        cvor_pridruzivanje = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_pridruzivanje = cvor.djeca[2]
            
            svojstva_argumenti = {}
            if not self.lista_argumenata( cvor.djeca[0], djelokrug,
                                        svojstva_argumenti ):
                return False
            
            tipovi = svojstva_argumenti['tipovi']
        
        svojstva_pridruzivanje = {}
        if not self.izraz_pridruzivanja( cvor_pridruzivanje, djelokrug,
                                        svojstva_pridruzivanje ):
            return False
        
        tipovi.append( svojstva_pridruzivanje['tip'] )
        
        izvedena_svojstva['tipovi'] = tipovi
        return True
    
    
    def unarni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = JednostavniTip( 'int' )
        l_izraz = False
        
        if len( cvor.djeca ) == 1:
            
            svojstva_postfiks = {}
            if not self.postfiks_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_postfiks ):
                return False
            
            tip = svojstva_postfiks['tip']
            l_izraz = svojstva_postfiks['l-izraz']
        
        elif cvor.djeca[1].nezavrsni_znak == '<unarni_izraz>':
            
            svojstva_unarni = {}
            if not self.unarni_izraz( cvor.djeca[1], djelokrug,
                                    svojstva_unarni ):
                return False
            
            if not svojstva_unarni['l-izraz'] or \
                not svojstva_unarni['tip'].je_li_svodivo( tip ):
                
                self.ispisi_produkciju( cvor )
                return False
        
        else:
            
            # u ovom slucaju cvor.djeca[0] je nezavrsni znak <unarni_operator>
            # njega ne treba provjeravati u semantickoj analizi
            
            svojstva_cast = {}
            if not self.cast_izraz( cvor.djeca[1], djelokrug, svojstva_cast ):
                return False
            
            if not svojstva_cast['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def cast_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        if len( cvor.djeca ) == 1:
            
            svojstva_unarni = {}
            if not self.unarni_izraz( cvor.djeca[0], djelokrug,
                                    svojstva_unarni ):
                return False
            
            tip = svojstva_unarni['tip']
            l_izraz = svojstva_unarni['l-izraz']
        
        else:
            
            svojstva_ime_tipa = {}
            if not self.ime_tipa( cvor.djeca[1], djelokrug, svojstva_ime_tipa ):
                return False
            
            svojstva_cast = {}
            if not self.cast_izraz( cvor.djeca[3], djelokrug, svojstva_cast ):
                return False
            
            if not svojstva_cast['tip'].je_li_svodivo_eksplicitno( 
                svojstva_ime_tipa['tip'] ):
                
                self.ispisi_produkciju( cvor )
                return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
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
    
    
    def multiplikativni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_cast = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_cast = cvor.djeca[2]
            
            svojstva_multiplikativni = {}
            if not self.multiplikativni_izraz( cvor.djeca[0], djelokrug,
                                                svojstva_multiplikativni ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_multiplikativni['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_cast = {}
        if not self.cast_izraz( cvor_cast, djelokrug, svojstva_cast ):
            return False
        
        if l_izraz is None:
            tip = svojstva_cast['tip']
            l_izraz = svojstva_cast['l-izraz']
        
        elif not svojstva_cast['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def aditivni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_multiplikativni = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_multiplikativni = cvor.djeca[2]
            
            svojstva_aditivni = {}
            if not self.aditivni_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_aditivni ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_aditivni['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_multiplikativni = {}
        if not self.multiplikativni_izraz( cvor_multiplikativni, djelokrug,
                                            svojstva_multiplikativni ):
            return False
        
        if l_izraz is None:
            tip = svojstva_multiplikativni['tip']
            l_izraz = svojstva_multiplikativni['l-izraz']
        
        elif not svojstva_multiplikativni['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def odnosni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_aditivni = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_aditivni = cvor.djeca[2]
            
            svojstva_odnosni = {}
            if not self.odnosni_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_odnosni ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_odnosni['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_aditivni = {}
        if not self.aditivni_izraz( cvor_aditivni, djelokrug,
                                    svojstva_aditivni ):
            return False
        
        if l_izraz is None:
            tip = svojstva_aditivni['tip']
            l_izraz = svojstva_aditivni['l-izraz']
        
        elif not svojstva_aditivni['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def jednakosni_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_odnosni = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_odnosni = cvor.djeca[2]
            
            svojstva_jednakosni = {}
            if not self.jednakosni_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_jednakosni ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_jednakosni['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_odnosni = {}
        if not self.odnosni_izraz( cvor_odnosni, djelokrug, svojstva_odnosni ):
            return False
        
        if l_izraz is None:
            tip = svojstva_odnosni['tip']
            l_izraz = svojstva_odnosni['l-izraz']
        
        elif not svojstva_odnosni['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def bin_i_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_jednakosni = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_jednakosni = cvor.djeca[2]
            
            svojstva_bi = {}
            if not self.bin_i_izraz( cvor.djeca[0], djelokrug, svojstva_bi ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_bi['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_jednakosni = {}
        if not self.jednakosni_izraz( cvor_jednakosni, djelokrug,
                                    svojstva_jednakosni ):
            return False
        
        if l_izraz is None:
            tip = svojstva_jednakosni['tip']
            l_izraz = svojstva_jednakosni['l-izraz']
        
        elif not svojstva_jednakosni['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def bin_xili_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_bin_i = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_bin_i = cvor.djeca[2]
            
            svojstva_xili = {}
            if not self.bin_xili_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_xili ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_xili['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_bi = {}
        if not self.bin_i_izraz( cvor_log_i, djelokrug, svojstva_bi ):
            return False
        
        if l_izraz is None:
            tip = svojstva_bi['tip']
            l_izraz = svojstva_bi['l-izraz']
        
        elif not svojstva_bi['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def bin_ili_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_bin_xi = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_bin_xi = cvor.djeca[2]
            
            svojstva_ili = {}
            if not self.bin_ili_izraz( cvor.djeca[0], djelokrug, svojstva_ili ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_ili['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_bxi = {}
        if not self.bin_xili_izraz( cvor_bin_xi, djelokrug, svojstva_bxi ):
            return False
        
        if l_izraz is None:
            tip = svojstva_bxi['tip']
            l_izraz = svojstva_bxi['l-izraz']
        
        elif not svojstva_bxi['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def log_i_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_bin_ili = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_bin_ili = cvor.djeca[2]
            
            svojstva_i = {}
            if not self.log_ili_izraz( cvor.djeca[0], djelokrug, svojstva_i ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_i['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_bili = {}
        if not self.bin_ili_izraz( cvor_bin_ili, djelokrug, svojstva_bili ):
            return False
        
        if l_izraz is None:
            tip = svojstva_bili['tip']
            l_izraz = svojstva_bili['l-izraz']
        
        elif not svojstva_bili['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def log_ili_izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        cvor_log_i = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_log_i = cvor.djeca[2]
            
            svojstva_ili = {}
            if not self.log_ili_izraz( cvor.djeca[0], djelokrug, svojstva_ili ):
                return False
            
            tip = JednostavniTip( 'int' )
            
            if not svojstva_ili['tip'].je_li_svodivo( tip ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = False
        
        svojstva_i = {}
        if not self.log_i_izraz( cvor_log_i, djelokrug, svojstva_i ):
            return False
        
        if l_izraz is None:
            tip = svojstva_i['tip']
            l_izraz = svojstva_i['l-izraz']
        
        elif not svojstva_i['tip'].je_li_svodivo( tip ):
            self.ispisi_produkciju( cvor )
            return False
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def izraz_pridruzivanja( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        tip = None
        l_izraz = None
        
        if len( cvor.djeca ) == 1:
            
            svojstva_log_ili = {}
            if not self.log_ili_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_log_ili ):
                return False
            
            tip = svojstva_log_ili['tip']
            l_izraz = svojstva_log_ili['l-izraz']
        
        else:
            
            svojstva_postfiks = {}
            if not self.postfiks_izraz( cvor.djeca[0], djelokrug,
                                        svojstva_postfiks ):
                return False
            
            if not svojstva_postfiks['l-izraz']:
                self.ispisi_produkciju( cvor )
                return False
            
            tip = svojstva_postfiks['tip']
            
            svojstva_pridruzivanje = {}
            if not self.izraz_pridruzivanja( cvor.djeca[2], djelokrug,
                                            svojstva_pridruzivanje ):
                return False
            
            if not tip.je_li_svodivo( svojstva_pridruzivanje['tip'] ):
                self.ispisi_produkciju( cvor )
                return False
            
            l_izraz = 0
        
        izvedena_svojstva['tip'] = tip
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
    def izraz( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        cvor_pridruzivanje = cvor.djeca[0]
        l_izraz = None
        
        if len( cvor.djeca ) > 1:
            
            cvor_pridruzivanje = cvor.djeca[2]
            
            l_izraz = False
            
            svojstva_izraz = {}
            if not self.izraz( cvor.djeca[0], djelokrug, svojstva_izraz ):
                return False
        
        svojstva_pridruzivanje = {}
        if not self.izraz_pridruzivanja( cvor_pridruzivanje, djelokrug,
                                        svojstva_pridruzivanje ):
            return False
        
        if l_izraz is None:
            l_izraz = svojstva_pridruzivanje['l-izraz']
        
        izvedena_svojstva['tip'] = svojstva_pridruzivanje['tip']
        izvedena_svojstva['l-izraz'] = l_izraz
        return True
    
    
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
        
        tip_int = JednostavniTip( 'int' )
        
        svojstva_izraz = {}
        if not self.izraz( cvor.djeca[2], djelokrug, svojstva_izraz ):
            return False
        
        if not svojstva_izraz['tip'].je_li_svodivo( tip_int ):
            self.ispisi_produkciju( cvor )
            return False
        
        # naredba prije eventualnog else
        if not self.naredba( cvor.djeca[4], djelokrug ):
            return False
            
        # slucaj else
        if len( cvor.djeca ) == 7:
            
            if not self.naredba( cvor.djeca[6], djelokrug ):
                return False
        
        return True
    
    
    def naredba_petlje( self, cvor, djelokrug ):
        
        tip_int = JednostavniTip( 'int' )
        
        # while petlja
        if cvor.djeca[0].uniformni_znak == 'KR_WHILE':
            
            svojstva_izraz = {}
            if not self.izraz( cvor.djeca[2], djelokrug, svojstva_izraz ):
                return False
            
            if not svojstva_izraz['tip'].je_li_svodivo( tip_int ):
                self.ispisi_produkciju( cvor )
                return False
            
            if not self.naredba( cvor.djeca[4], djelokrug ):
                return False
        
        # for petlja kraca verzija
        else:
            
            if not self.izraz_naredba( cvor.djeca[2], djelokrug ):
                return False
            
            svojstva2 = {}
            if not self.izraz_naredba( cvor.djeca[3], djelokrug, svojstva2 ):
                return False
            
            if not svojstva2['tip'].je_li_svodivo( tip_int ):
                self.ispisi_produkciju( cvor )
                return False
            
            cvor_naredba = cvor.djeca[5]
            
            # for sa izrazom na trecem mjestu
            if len( cvor.djeca ) == 7:
                
                cvor_naredba = cvor.djeca[6]
                
                if not self.izraz( cvor.djeca[4], djelokrug ):
                    return False
            
            if not self.naredba( cvor_naredba, djelokrug ):
                return False
        
        return True
    
    
    def naredba_skoka( self, cvor, djelokrug ):
        # TODO
        return True
    
    
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
        if ime in self.funkcije_bez_definicije.keys():
            
            self.funkcije_bez_definicije[ ime ].discard( tip_funkcije )
            
            if len( self.funkcije_bez_definicije[ ime ] ) == 0:
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
        
        cvor_deklaracija = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_deklaracija = cvor.djeca[1]
            
            if not self.lista_deklaracija( cvor.djeca[0], djelokrug ):
                return False
        
        return self.deklaracija( cvor_deklaracija, djelokrug )
    
    
    def deklaracija( self, cvor, djelokrug ):
        
        svojstva_tip = {}
        if not self.ime_tipa( cvor.djeca[0], svojstva_tip ):
            return False
        
        return self.lista_init_deklaratora( cvor.djeca[1], djelokrug,
                                        svojstva_tip['tip'] )
    
    
    def lista_init_deklaratora( self, cvor, djelokrug, ntip ):
        '''ntip je nasljedno svojstvo'''
        
        cvor_deklarator = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_deklarator = cvor.djeca[2]
            
            if not self.lista_init_deklaratora( cvor.djeca[0], djelokrug,
                                                ntip ):
                return False
        
        return self.init_deklarator( cvor_deklarator, djelokrug, ntip )
    
    
    def init_deklarator( self, cvor, djelokrug, ntip ):
        '''ntip je nasljedno svojstvo'''
        
        svojstva_izravni = {}
        if not self.izravni_deklarator( cvor.djeca[0], djelokrug, ntip,
                                    svojstva_izravni ):
            return False
        
        if len( cvor.djeca ) == 1:
            if svojstva_izravni['tip'].je_li_const():
                return False
        
        # slucaj sa inicijalizatorom
        else:
            
            svojstva_inicijalizator = {}
            if not self.inicijalizator( cvor.djeca[2], djelokrug,
                                        svojstva_inicijalizator ):
                return False
            
            # TODO provjere tipova inicijalizatora
        
        return True
    
    
    def izravni_deklarator( self, cvor, djelokrug, ntip,
                            izvedena_svojstva = {} ):
        '''ntip je nasljedno svojstvo'''
        
        ime = cvor.djeca[0].leksicka_jedinka
        
        # brojevni tip
        if len( cvor.djeca ) == 1:
            
            if ntip.je_li_void():
                self.ispisi_produkciju( cvor )
                return False
            
            if djelokrug.postoji_li_ime_lokalno( ime ):
                self.ispisi_produkciju( cvor )
                return False
            
            djelokrug.dodaj( ime, ntip )
            izvedena_svojstva['tip'] = ntip
            return True
        
        # niz
        elif cvor.djeca[1].uniformni_znak == 'L_UGL_ZAGRADA':
            
            if ntip.je_li_void():
                self.ispisi_produkciju( cvor )
                return False
            
            if djelokrug.postoji_li_ime_lokalno( ime ):
                self.ispisi_produkciju( cvor )
                return False
            
            broj_elemenata = int( cvor.djeca[2].leksicka_jedinka )
            
            if broj_elemenata <= 0 or broj_elemenata > 1024:
                self.ispisi_produkciju( cvor )
                return False
            
            tip = TipNiz( ntip )
            
            djelokrug.dodaj( ime, tip )
            izvedena_svojstva['tip'] = tip
            izvedena_svojstva['br-elem'] = broj_elemenata
            return True
        
        # funkcija
        
        domena = JednostavniTip( 'void' )
        
        if type( cvor.djeca[2] ) == NezavrsniZnak:
            
            svojstva_parametri = {}
            if not self.lista_parametara( cvor.djeca[2], svojstva_parametri ):
                return False
            
            domena = svojstva_parametri['tipovi']
        
        tip_funkcije = TipFunkcija( domena, ntip )
        
        # ako ima deklaracija ovog imena, je li to funkcija istog tipa?
        if not djelokrug.provjeri_funkciju( ime, tip_funkcije ):
            self.ispisi_produkciju( cvor )
            return False
        
        # ako nema deklaracija, dodaj ju
        if not djelokrug.postoji_li_ime_lokalno( ime ):
            djelokrug.dodaj( ime, tip_funkcije )
        
        # provjere za definicije funkcija: ako ne postoji definicija, zabiljezi
        if ( ime not in self.definirane_funkcije.keys() ) or \
            ( tip_funkcije != self.definirane_funkcije[ ime ] ):
            
            if ime not in self.funkcije_bez_definicije.keys():
                self.funkcije_bez_definicije[ ime ] = { tip_funkcije }
            else:
                self.funkcije_bez_definicije[ ime ].add( tip )
        
        izvedena_svojstva['tip'] = tip_funkcije
        return True
    
    
    def inicijalizator( self, cvor, djelokrug, izvedena_svojstva = {} ):
        
        if len( cvor.djeca ) == 1:
            
            svojstva_pridruzivanje = {}
            if not self.izraz_pridruzivanja( cvor.djeca[0], djelokrug,
                                            svojstva_pridruzivanje ):
                return False
            
            listovi = self.dohvati_listove( cvor.djeca[0] )
            
            self.pisi( listovi )
            
            if len( listovi ) == 1 and \
                listovi[0].uniformni_znak == 'NIZ_ZNAKOVA':
                
                br_elem = self.izbroji_znakove( listovi[0].leksicka_jedinka )
                br_elem += 1 # ZA ZAVRSNI '\0' ZNAK
                
                tipovi = [ JednostavniTip( 'char' ) ] * br_elem
                
                izvedena_svojstva['br-elem'] = br_elem
                izvedena_svojstva['tipovi'] = tipovi
            
            else:
                izvedena_svojstva['tip'] = svojstva_pridruzivanje['tip']
        
        else:
            
            svojstva_lista = {}
            if not self.lista_izraza_pridruzivanja( cvor.djeca[1], djelokrug,
                                                    svojstva_lista ):
                return False
            
            izvedena_svojstva['br-elem'] = svojstva_lista['br-elem']
            izvedena_svojstva['tipovi'] = svojstva_lista['tipovi']
        
        return True
    
    
    def lista_izraza_pridruzivanja( self, cvor, djelokrug,
                                    izvedena_svojstva = {} ):
        
        tipovi = []
        br_elem = 0
        
        cvor_pridruzivanje = cvor.djeca[0]
        
        if len( cvor.djeca ) > 1:
            
            cvor_pridruzivanje = cvor.djeca[2]
            
            svojstva_lista = {}
            if not self.lista_izraza_pridruzivanja( cvor.djeca[0], djelokrug,
                                                    svojstva_lista ):
                return False
            
            tipovi = svojstva_lista['tipovi']
            br_elem = svojstva_lista['br-elem']
        
        svojstva_pridruzivanje = {}
        if not self.izraz_pridruzivanja( cvor_pridruzivanje, djelokrug,
                                        svojstva_pridruzivanje ):
            return False
        
        tipovi.append( svojstva_pridruzivanje['tip'] )
        br_elem += 1
        
        izvedena_svojstva['tipovi'] = tipovi
        izvedena_svojstva['br-elem'] = br_elem
        return True
    
    
    ######################### DODATNE POMOCNE METODE ###########################
    
    
    def dohvati_listove( self, cvor ):
        
        listovi = []
        
        for dijete in cvor.djeca:
            
            if type( dijete ) == LeksickaJedinka:
                listovi.append( dijete )
            
            else:
                listovi.append( self.dohvati_listove( dijete ) )
        
        return listovi
    
    
    def izbroji_znakove( self, niz_znakova ):
        
        prefiksirano = False
        broj = 0
        
        for znak in niz_znakova[1:-1]:
            
            if prefiksirano:
                prefiksirano = False
                
                broj += 1
            
            else:
                if znak == '\\':
                    prefiksirano = True
                else:
                    broj += 1
        
        return broj
