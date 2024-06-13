from regex import *
from HulkGrammar import *
from Parser import *
class Token:

    def __init__(self, line, column, type_, lex):
        self.line = line
        self.column = column
        self.type_ = type_
        self.lex = lex

Terminal_symb = {
    '=>': flecha,
    ';': punto_c,
    '{': llave_a,
    '}': llave_c,
    '(': opar,
    ')': cpar,
    '&': and_,
    '|': or_,
    '!': not_,
    '<': menor,
    '<=': menor_e,
    '>': mayor,
    '>=': mayor_e,
    '==': equal,
    '!=': distinto,
    '+': plus,
    '-': minus,
    '@': arroba,
    '@@': arroba_d,
    '*': star,
    '/': div,
    '%': resto,
    '^': pow_,
    ',': coma,
    '=': asignar,
    ':=': asignar_d,
    ':': dos_p,
    '.': punto,
    '[': colchete_a,
    ']': colchete_c,
    '||': doble_or
}

Terminal_res = {
    'function': function,
    'type': type_,
    'inherits': inherits,
    'protocol': protocol,
    'extends': extends,
    'let': let,
    'in': in_,
    'if': if_,
    'elif': elif_,
    'else': else_,
    'while': while_,
    'for': for_,
    'is': is_,
    'as': as_,
    'new': new_,
    'True': bool_,
    'False': bool_
}

symbols = regex([escape,or_1, or_1, escape, por,or_1, escape, mas,or_1, escape, colchete_a1, or_1, escape, colchete_c1, or_1, escape, opar1, or_1, escape, cpar1, or_1, escape, menos1, or_1, g_bajo, or_1, punto1, or_1, punto_c1, or_1, llave_a1, or_1, llave_c1, or_1, coma1, or_1, igual1, or_1, div1, or_1, porcentaje,or_1, pow1, or_1, dos_p1, or_1, arroba1, or_1, and1, or_1, not_1, or_1, escape,or_1, escape,or_1, or_1,mayor1,or_1, menor1 , or_1, igual1, igual1, or_1, menor1, igual1, or_1, mayor1, igual1, or_1, igual1, igual1, or_1, not_1, igual1,or_1, igual1, mayor1, or_1, dos_p1, igual1, or_1, arroba1, arroba1,R.EOF])

'0.[0-9]+|[1-9][0-9]*|[1-9][0-9]*.[0-9]+|0'
numbers = regex([cero,punto1, colchete_a1, cero, guion, nueve, colchete_c1,mas,or_1, colchete_a1, uno, guion, nueve, colchete_c1, colchete_a1, cero, guion, nueve, colchete_c1, por, or_1, colchete_a1, uno, guion, nueve, colchete_c1, colchete_a1, cero, guion, nueve, colchete_c1, por, punto1, colchete_a1, cero, guion, nueve, colchete_c1, mas,or_1, cero,R.EOF])


'[_-_a-zA-Z][_-_a-zA-Z0-9]*'
identifier = regex([colchete_a1, g_bajo, guion, g_bajo, aa, guion, zz, A, guion, Z,colchete_c1, colchete_a1, g_bajo, guion, g_bajo, aa, guion, zz, A, guion, Z,cero, guion, nueve, colchete_c1, por, R.EOF])


def tokenizer(input):
    tokens = []
    input = input.rstrip()

    line = 1
    column = 1

    while len(input):

        while input[0].isspace():
            if input[0] == '\n':
                line = line + 1
                column = 1
            else:
                column = column + 1

            input = input[1:]

        check, indice, lex = symbols.match(input)
        if check == True:
            tokens.append(Token(line, column, Terminal_symb[lex], lex))

            column += indice
            input = input[indice:]

            continue
        check, indice, lex = numbers.match(input)

        if check == True:
            tokens.append(Token(line, column, num, float(lex)))
            column += indice
            input = input[indice:]

            continue

        check, indice, lex = identifier.match(input)
        if check == True:
            if lex in Terminal_res:
                tokens.append(Token(line, column, Terminal_res[lex], lex))
            else:
                tokens.append(Token(line, column, Id, lex))
            
            column = column + 1
            input = input[indice:]

            continue

        if input[0] == '"':
            indice = 1

            while input[indice] != '"':
                if input[indice] == '\\':
                    indice += 1

                indice += 1
            
            tokens.append(Token(line, column, str_, input[1:indice]))

            column = column + indice
            input = input[indice + 1:]

            continue

        #if input[0] == '#':
        #    while input[0] != '\n':
        #        column += 1
        #        input = input[1:]

        #    continue

        raise SyntaxError(f'Invalid syntax at {line}:{column}')
    tokens.append(Token(line, column, G.EOF, G.EOF))
    return tokens

d = tokenizer('''
    {
    let squares = [x^2 || x in range(1, 10)] in print(x);
    7 + 4;
    };
''')
parse = slr_parser(G, lambda x: x.type_)
derivation = parse(d)
print(derivation.expression)