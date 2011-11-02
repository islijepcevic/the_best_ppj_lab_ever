'''This is the automat model of the lexycal analyzer

created: 11. 10. 2011
Ivan Slijepcevic
'''

from generator.regularexpression import RegularExpression

class AutomatModel():
    '''this class represents the automat model of the lexycal analyzer
the basic idea is to construct a transition table from this model for the
executeable version of the automat - the lexycal analyzer
'''
    
    def __init__( self, reg_def, stanja, lex, pravila ):
        '''constructor'''
        
        self.regdef = reg_def # dict k: ime definicije; val: regex
        self.stanja = stanja # list stringova
        self.lex_units = lex # list stringova
        self.pravila = pravila # list objekata AnalyzerRule()
        
        self.prijelazi = {} # key: (stanje, znak); value: [stanja]
        self.br_stanja = 1
        self.pocetno_stanje = 0
        # svako prihvatljivo stanje je jedan regularni izraz
        self.prihvatljiva_stanja = []
        # stanja analizatora uz svaki regularni izraz
        self.stanja_analizatora = []
        
        self.akcije = {}
    
    
    def dispose( self ):
        del self.prijelazi
        del self.pravila
        del self.lex_units
        del self.stanja
        del self.regdef
    
    
    def napravi_analizator( self ):
        
        for pravilo in self.pravila:
            regex = pravilo.regular_expression
            
            (lijevo, desno) = self.pretvori(regex)
            
            self.dodaj_epsilon_prijelaz( self.pocetno_stanje, lijevo )
            self.prihvatljiva_stanja.append( desno )
            
            stanje = pravilo.state_name
            akcije = pravilo.actions_to_list()
            
            self.stanja_analizatora.append( stanje )
            self.akcije[ (stanje, desno) ] = akcije
        
        upute = 'R' + str( self.prihvatljiva_stanja ) + '\n'
        upute += 'A' + str( self.akcije ) + '\n'
        upute += 'S' + str( self.br_stanja ) + '\n'
        upute += 'P' + str( self.pocetno_stanje ) + '\n'
        upute += 'T' + str( self.prijelazi ) + '\n'
        upute += 'Z' + str( self.stanja_analizatora ) + '\n'
        upute += 'I' + str( self.stanja[0] ) + '\n'
        
        analyzer_stream = open( 'analizator/analizator.upute', 'w' )
        analyzer_stream.write( upute )
        analyzer_stream.close()
    
    
    def dodaj_prijelaz( self, stanje, novo_stanje, znak ):
        
        if (stanje, znak) not in list( self.prijelazi.keys() ):
            self.prijelazi[ (stanje, znak) ] = [ novo_stanje ]
        else:
            self.prijelazi[ (stanje, znak) ].append( novo_stanje )
    
    
    def dodaj_epsilon_prijelaz( self, stanje, novo_stanje ):
        self.dodaj_prijelaz( stanje, novo_stanje, 'epsilon' )
    
    
    def novo_stanje( self ):
        
        self.br_stanja += 1
        return self.br_stanja - 1
    
    
    def pretvori( self, regex ):
        
        if type(regex) == str:
            regex = RegularExpression( regex )
        
        izbori = list()
        x = 0
        br_zagrada = 0
        br2_zagrada = 0
        br_op_izbora = 0
        
        for i in range(len(regex)):
            if regex[i] == '(' and regex.jest_operator( i ):
                br_zagrada += 1
            elif regex[i] == ')' and regex.jest_operator ( i ):
                br_zagrada -= 1
            elif br_zagrada == 0 and regex[i] == '|' and regex.jest_operator(i):
                
                izbori.append(regex[x:i])
                br_op_izbora +=1
                x = i + 1

        if br_op_izbora > 0:
            izbori.append(regex[x:])
            
        lijevo_stanje = self.novo_stanje()
        desno_stanje = self.novo_stanje()
        
        if br_op_izbora > 0:
            for i in range(len(izbori)):
                (privremeno_lijevo, privremeno_desno) = self.pretvori(izbori[i])
                self.dodaj_epsilon_prijelaz(lijevo_stanje, privremeno_lijevo)
                self.dodaj_epsilon_prijelaz(privremeno_desno, desno_stanje)
                
        # nema operatora izbora
        else:
            prefiksirano = False
            trenutno_stanje = lijevo_stanje
            preskoci = False
            j = 0
            for i in range(len(regex)):
                
                if i <= j and i != 0: continue
                if preskoci is True:
                    preskoci = False
                    continue

                if prefiksirano is True:
                    prefiksirano = False
                    prijelazni_znak = ''
                    if regex[i] == 't': prijelazni_znak = '\t'
                    elif regex[i] == 'n': prijelazni_znak = '\n'
                    elif regex[i] == '_': prijelazni_znak = ' '
                    else: prijelazni_znak = regex[i]

                    sljedece_stanje = self.novo_stanje()
                    self.dodaj_prijelaz (trenutno_stanje, sljedece_stanje, prijelazni_znak)

                    if (i+1) < len(regex) and regex[i+1] == '*':
                        self.dodaj_epsilon_prijelaz (sljedece_stanje, trenutno_stanje)
                        dodatno_stanje = self.novo_stanje()
                        self.dodaj_epsilon_prijelaz( trenutno_stanje, dodatno_stanje )
                        self.dodaj_epsilon_prijelaz( sljedece_stanje, dodatno_stanje )
                        preskoci = True
                        
                        sljedece_stanje = dodatno_stanje
                    
                    trenutno_stanje = sljedece_stanje
                
                # nije prefiksirano
                else:
                    if regex[i] == '\\':
                        prefiksirano = True
                        continue
                    
                    if regex[i] != '(':
                        sljedece_stanje = self.novo_stanje()
                        if regex[i] == '$':
                            self.dodaj_epsilon_prijelaz(trenutno_stanje, sljedece_stanje)
                        else:
                            self.dodaj_prijelaz(trenutno_stanje, sljedece_stanje, regex[i])

                        if (i+1) < len(regex) and regex[i+1] == '*':
                            self.dodaj_epsilon_prijelaz (sljedece_stanje, trenutno_stanje)
                            dodatno_stanje = self.novo_stanje()
                            self.dodaj_epsilon_prijelaz( trenutno_stanje, dodatno_stanje )
                            self.dodaj_epsilon_prijelaz( sljedece_stanje, dodatno_stanje )
                            preskoci = True
                            
                            sljedece_stanje = dodatno_stanje
                            
                        trenutno_stanje=sljedece_stanje
                        
                    # jest zagrada
                    else:
                        br2_zagrada += 1
                        for x in range((i+1), len(regex)):

                                if regex[x] == '(' and regex.jest_operator( x ):
                                        br2_zagrada +=1
                                elif regex[x] == ')' and regex.jest_operator(x):
                                        br2_zagrada -= 1
                                        if br2_zagrada == 0:
                                            j = x
                                            break
                                else: continue
                                
                        (privremeno_lijevo, privremeno_desno) = self.pretvori(regex[(i+1):j])
                        self.dodaj_epsilon_prijelaz(trenutno_stanje, privremeno_lijevo)
                        bivse_trenutno = trenutno_stanje
                        trenutno_stanje = privremeno_desno
                        
                        if (j+1) < len(regex) and regex[j+1] == '*':
                            self.dodaj_epsilon_prijelaz(privremeno_desno, privremeno_lijevo)
                            dodatno_stanje = self.novo_stanje()
                            self.dodaj_epsilon_prijelaz( bivse_trenutno, dodatno_stanje )
                            self.dodaj_epsilon_prijelaz( privremeno_desno, dodatno_stanje )
                            preskoci = True
                            
                            trenutno_stanje = dodatno_stanje
                    
            self.dodaj_epsilon_prijelaz(trenutno_stanje, desno_stanje)
        
        return (lijevo_stanje, desno_stanje)
