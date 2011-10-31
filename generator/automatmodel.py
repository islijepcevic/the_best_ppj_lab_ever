'''This is the automat model of the lexycal analyzer

created: 11. 10. 2011
Ivan Slijepcevic
'''

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
        self.br_stanja = 0
    
    
    def dispose( self ):
        del self.prijelazi
        del self.pravila
    
    
    def run( self ):
        
        for pravilo in self.pravila:
            regex = pravilo.get_regex()
            (lijevo, desno) = self.pretvori(regex)
            #nesto sto dodaje ostala pravila za akciju
        

    def dodaj_prijelaz( self, stanje, novo_stanje, znak ):
        
        if (stanje, znak) not in list( self.prijelazi.keys() ):
            self.prijelazi[ (stanje, znak) ] = [ novo_stanje ]
        else:
            self.prijelazi[ (stanje, znak) ].append( novo_stanje )

    def dodaj_epsilon_prijelaz( self, stanje, novo_stanje ):
        self.dodaj_prijelaz( stanje, novo_stanje, '$' )


    def novo_stanje( self ):
        
        self.br_stanja += 1
        return self.br_stanja - 1

    def je_operator( self, regex, i ):
        br = 0
        while(i-1 >= 0 and regex[i-1] == '\\'):
            br += 1
            i -= 1
        return br%2 == 0

    def pretvori( self, regex ):
     
        izbori = list()
        x = 0
        br_zagrada = 0
        br2_zagrada = 0
        br_op_izbora = 0
        
        for i in range(len(regex)):
            if regex[i] == '(' and self.je_operator(regex, i):
                br_zagrada += 1
            elif regex[i] == ')' and self.je_operator (regex, i):
                br_zagrada -= 1
            elif br_zagrada == 0 and regex[i] == '|' and self.je_operator(regex, i):
                
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
                        self.dodaj_epsilon_prijelaz (trenutno_stanje, sljedece_stanje)
                        self.dodaj_epsilon_prijelaz (sljedece_stanje, trenutno_stanje)
                        preskoci = True
                        
                    trenutno_stanje = sljedece_stanje
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
                            self.dodaj_epsilon_prijelaz (trenutno_stanje, sljedece_stanje)
                            self.dodaj_epsilon_prijelaz (sljedece_stanje, trenutno_stanje)
                            preskoci = True
                            
                        trenutno_stanje=sljedece_stanje
                        
                    else:
                        br2_zagrada += 1
                        for x in range((i+1), len(regex)):

                                if regex[x] == '(' and self.je_operator(regex, x):
                                        br2_zagrada +=1
                                elif regex[x] == ')' and self.je_operator(regex, x):
                                        br2_zagrada -= 1
                                        if br2_zagrada == 0:
                                            j = x
                                            break 
                                else: continue
                                
                        (privremeno_lijevo, privremeno_desno) = self.pretvori(regex[(i+1):j])
                        self.dodaj_epsilon_prijelaz(trenutno_stanje, privremeno_lijevo)
                        trenutno_stanje = privremeno_desno
                        
                        if (j+1) < len(regex) and regex[j+1] == '*':
                            self.dodaj_epsilon_prijelaz(privremeno_lijevo, privremeno_desno)
                            self.dodaj_epsilon_prijelaz(privremeno_desno, privremeno_lijevo)
                            preskoci = True
                    
            self.dodaj_epsilon_prijelaz(trenutno_stanje, desno_stanje)
        
        return (lijevo_stanje, desno_stanje)
