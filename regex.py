from Grammar import *
from AutomatonWork import *
from Parser import *
import string


R = Grammar()
#c = []
#d = []
#a = []
#
#
#gram_symbols = '|*+[]()-\\'
#for i in string.printable:
#    if i in gram_symbols:
#        continue
#    a.append(i)
#for i in gram_symbols:
#    d.append(R.Terminals(i))
S = R.NonTerminal('S', True)
Expression1, Termino1, Factor1, SubTermino, SubFactor, Range, Primitive, Character, Escape, Char = R.NonTerminals('Expression1 Termino1 Factor1 SubTermino SubFactor Range Primitive Character Escape Char')
#for i in a:
#    c.append(R.Terminals(i))
or_1, por, mas, colchete_a1, colchete_c1, opar1, cpar1, guion, escape, aa, zz, A,Z, g_bajo, cero, nueve, uno, punto1, punto_c1, llave_a1, llave_c1, coma1, igual1,menos1, div1,porcentaje, pow1, dos_p1, arroba1, and1, not_1, or_d1, mayor1, menor1 = R.Terminals('| * + [ ] ( ) - \\ a z A Z _ 0 9 1 . ; { } , = - / % ^ : @ & ! || > <')
S %= Expression1, lambda s: s[0]

Expression1 %= Expression1 + or_1 + Termino1, lambda s: Or_(s[1], s[3]), None, None, None
Expression1 %= Termino1, lambda s: s[1], None

Termino1 %= Termino1 + Factor1, lambda s: Sum(s[1], s[2]), None, None
Termino1 %= Factor1, lambda s: s[1], None

Factor1 %= Range + por, lambda s: Kleen_star(incognit(s[1])), None, None
Factor1 %= Range + mas, lambda s: Sum(s[1], Kleen_star(incognit(s[1]))), None, None
Factor1 %= Range, lambda s: s[1], None

Range %= colchete_a1 + SubTermino + colchete_c1, lambda s: s[2], None, None, None
Range %= Character, lambda s: s[1], None
Range %= opar1 + Expression1 + cpar1, lambda s: s[2], None, None, None

SubTermino %= SubTermino + SubFactor, lambda s: Or_(s[1], s[2]), None, None
SubTermino %= SubFactor, lambda s: s[1], None

SubFactor %= Character + guion + Character, lambda s: range_(s[1], s[3]), None, None, None

Character %= Escape, lambda s: s[1], None
Character %= Char, lambda s: s[1], None

Char %= aa, lambda s: character(str(s[1])), None
Char %= zz, lambda s: character(str(s[1])), None
Char %= A, lambda s: character(str(s[1])), None
Char %= Z, lambda s: character(str(s[1])), None
Char %= cero, lambda s: character(str(s[1])), None
Char %= nueve, lambda s: character(str(s[1])), None
Char %= uno, lambda s: character(str(s[1])), None
Char %= g_bajo, lambda s: character(str(s[1])), None
Char %= punto1,lambda s: character(str(s[1])), None
Char %= punto_c1,lambda s: character(str(s[1])), None
Char %= llave_a1,lambda s: character(str(s[1])), None
Char %= llave_c1,lambda s: character(str(s[1])), None
Char %= coma1,lambda s: character(str(s[1])), None
Char %= igual1,lambda s: character(str(s[1])), None
Char %= div1,lambda s: character(str(s[1])), None
Char %= porcentaje,lambda s: character(str(s[1])), None
Char %= pow1,lambda s: character(str(s[1])), None
Char %= dos_p1,lambda s: character(str(s[1])), None
Char %= arroba1,lambda s: character(str(s[1])), None
Char %= and1,lambda s: character(str(s[1])), None
Char %= or_d1,lambda s: character(str(s[1])), None
Char %= not_1,lambda s: character(str(s[1])), None
Char %= mayor1,lambda s: character(str(s[1])), None
Char %= menor1,lambda s: character(str(s[1])), None

Escape %= escape + or_1, lambda s: character(str(s[2])), None, None
Escape %= escape + por, lambda s: character(str(s[2])), None, None
Escape %= escape + mas, lambda s: character(str(s[2])), None, None
Escape %= escape + colchete_a1, lambda s: character(str(s[2])), None, None
Escape %= escape + colchete_c1, lambda s: character(str(s[2])), None, None
Escape %= escape + opar1, lambda s: character(str(s[2])), None, None
Escape %= escape + cpar1, lambda s: character(str(s[2])), None, None
Escape %= escape + menos1, lambda s: character(str(s[2])), None, None
Escape %= escape + escape, lambda s: character(str(s[2])), None, None
Escape %= escape + or_d1, lambda s: character(str(s[2])), None, None
parse_regex = slr_parser(R, lambda x: x)

l = parse_regex([colchete_a1, cero, guion, nueve, colchete_c1, mas, or_1, colchete_a1, cero, guion, nueve, colchete_c1, por, punto1, colchete_a1, cero, guion, nueve, colchete_c1, mas,  R.EOF])
'| * + [ ] ( ) - \\ a z A Z _ 0 9 1 . ; { } , = - / % ^ : @ & ! || > <'
a = parse_regex([escape,or_1, or_1, escape, por,or_1, escape, mas,or_1, escape, colchete_a1, or_1, escape, colchete_c1, or_1, escape, opar1, or_1, escape, cpar1, or_1, escape, menos1, or_1, g_bajo, or_1, punto1, or_1, punto_c1, or_1, llave_a1, or_1, llave_c1, or_1, coma1, or_1, igual1, or_1, div1, or_1, porcentaje,or_1, pow1, or_1, dos_p1, or_1, arroba1, or_1, and1, or_1, not_1, or_1,or_d1, or_d1, or_1,mayor1,or_1, menor1 , R.EOF])
#c = build_lexer(a)
#l = build_lexer(l)
#mm, m1 = c(['||'])
#print(mm, m1)
#mm, m1 = l(['3', '4'])
#print(mm, m1)
class regex:
    def __init__(self, cadena):
        self.aut = parse_regex(cadena)##### + [0]
        #print(self.aut.transitions)
        self.recognize = build_lexer(self.aut)

    def match(self, cadena):
        count, c = self.recognize(list(cadena) + [0]) #### + [0]

        return count, c + 1, cadena[:c + 1]