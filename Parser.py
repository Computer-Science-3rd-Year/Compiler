from Grammar import *
import copy
from HulkGrammar import *
# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    allEpsilon = True
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    #                   <CODE_HERE>                   #
    ###################################################
    for s in alpha:
        for item in firsts[s]:
            first_alpha.add(item)
        if not firsts[s].contains_epsilon:
            allEpsilon = False
            break
    if allEpsilon:
        first_alpha.set_epsilon(True)
           
    ###################################################
    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
    ###################################################
    #                   <CODE_HERE>                   #
    ###################################################
    
    # First(alpha)
    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

#firsts = compute_firsts(G)


def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################
            #                   <CODE_HERE>                   #
            ###################################################
            for i, item in enumerate(alpha):
                if item in G.terminals:
                    continue
                
                first1 = compute_local_first(firsts, alpha[i+1:])
                #follows[item] = follows[item].Union(first1)
                for a in first1:
                    b = follows[item].add(a)
                    if b:
                        change = True
                if first1.contains_epsilon or i == len(alpha) - 1:
                    for c in follow_X:
                        d = follows[item].add(c)
                        if d:
                            change = True
    # Follow(Vn)
    return follows

#follows = compute_follows(G, firsts)

def lr0_closure(G,item):
    closure = {item}
    
    x = True
    while x:

        len_c = len(closure)

        for produc, pos in closure.copy():
            right = G.Productions[produc].Right

            if len(right) + 1 == pos:
                continue
            
            if right[pos - 1] in G.nonTerminals:
                for k in range(1, len(G.Productions)):
                    if right[pos - 1] == G.Productions[k].Left:
                        closure.add((k,1))
        x = len(closure) != len_c
    return closure

def lr0_goto(G,closure, symbol):
    newclosure = set()

    for production, pos in closure:
        right = G.Productions[production].Right
        if len(right) + 1 == pos:
            continue

        if right[pos - 1] == symbol:
            newclosure.update(lr0_closure(G,(production, pos + 1)))
    
    return newclosure

def slr_parser_table(G):
    canonical = [0, lr0_closure(G,(0,1))]
    action = {}
    goto = {}
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    c = 1
    while c < len(canonical):

        for d in G.terminals:

            closure = lr0_goto(G,canonical[c], d)
            if len(closure):
                try:
                    k = canonical.index(closure)
                except ValueError:
                    k = len(canonical)
                    canonical.append(closure)
                    #print(closure, d)
                if (c,d) in action:
                    action[(c,d)].append(k)
                else:
                    action[(c,d)] = [k]

        for d in G.nonTerminals:
            closure = lr0_goto(G,canonical[c], d)

            if len(closure):
                try:
                    k = canonical.index(closure)
                except ValueError:
                    k = len(canonical)
                    canonical.append(closure)
                if (c,d) in goto:
                    goto[(c,d)].append(k)
                else:
                    goto[(c,d)] = [k]
        for k, pos in canonical[c]:
            
            Production = G.Productions[k]
            left = Production.Left
            right = Production.Right

            if len(right) + 1 == pos:
                if not k:
                    if (c,G.EOF) in action:
                        action[(c,G.EOF)].append(0)
                    else:
                        action[(c,G.EOF)] = [0]
                else:
                    for a in follows[left]:
                        if (c,a) in action:
                            if negativos(action[(c,a)]):
                                action[(c,a)].append(-k)
                            else:
                                action[(c,a)] = [-k]
                        else:                            action[(c,a)] = [-k]
        c += 1

    return goto, action

def slr_parser(G, funcion):

    goto, action = slr_parser_table(G)
    #for item in action:
    #    print(item, action[item])
    def parser(tokens):
        c = 0
        s = [1]
        r = []
        T = []
        while True:
            try:
                #print(s[-1], tokens[c])
                k = action[(s[-1], funcion(tokens[c]))][0]
            except:
                raise SyntaxError('No esta bien el codigo pasado')
            
            if not k:
                return r[0]
            if k > 0:
                s.append(k)
                r.append(tokens[c])
                c = c + 1
            else:
                left = G.Productions[-k].Left
                right = G.Productions[-k].Right
                reduce = G.Productions[-k].attributes[0]

                s_len = len(s) - len(right)
                s[s_len:] = []
               # print(r)
               # for i in r:
                #    if type(i) != Terminal and type(i) != int:
                #        print(i.transitions)
                args = copy.deepcopy(r[s_len - 1:])
                r[s_len - 1:] = []
                args.insert(0,0)
                r.append(reduce(args))
                T.append(G.Productions[-k])
                #print(G.Productions[-k])
                s.append(goto[(s[-1], left)][0])
    return parser
def negativos(array):
    return any(elemento < 0 for elemento in array)
#parse = slr_parser(G, lambda x: x.type_)
#derivation = parse([type_, Id, llave_a, Id, asignar, num, punto_c, llave_c, let, Id, asignar, num, in_, num,plus, num, punto_c, G.EOF])
#derivation = parse([type_, Id, opar, Id, cpar, llave_a, Id, asignar, num, punto_c, llave_c, num,punto_c, G.EOF])
#print(derivation)

