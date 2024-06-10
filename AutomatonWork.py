import copy
from regex import R

class Nfa:
    def __init__(self, q_0 = 0, q_f = 1, states = 2, transitions = {}, **args):
        self.q_0 = q_0
        self.q_f = q_f
        self.states = states
        self.transitions = transitions
        self.__dict__.update(args)    

def Or_(aut1, aut2):
    aux = copy.deepcopy(aut1)

    aux.q_f = aut1.states + aut2.q_f
    aux.states = aux.states + aut2.states

    if aut1.q_0 in aux.transitions:
        if '' in aux.transitions[aut1.q_0]:
            aux.transitions[aut1.q_0][''].append(aut1.states)
        else:
            aux.transitions[aut1.q_0][''] = [aut1.states]
    else:
        aux.transitions[aut1.q_0] = {}
        aux.transitions[aut1.q_0][''] = [aut1.states]

    if aut1.q_f in aux.transitions:
        if '' in aux.transitions[aut1.q_f]:
            aux.transitions[aut1.q_f][''].append(aux.q_f)
        else:
            aux.transitions[aut1.q_f][''] = [aux.q_f]
    else:
        aux.transitions[aut1.q_f] = {}
        aux.transitions[aut1.q_f][''] = [aux.q_f]
    
    for i in aut2.transitions.keys():
        for j in aut2.transitions[i].keys():
            c = [d + aut1.states for d in aut2.transitions[i][j]]
            if (i + aut1.states) in aux.transitions:
                if j in aux.transitions[i + aut1.states]:
                    aux.transitions[i + aut1.states][j].extend(c)
                else:
                    aux.transitions[i + aut1.states][j] = c
            else:
                aux.transitions[i + aut1.states] = {}
                aux.transitions[i + aut1.states][j] = c
    return aux

def Sum(aut1, aut2):

    aux = copy.deepcopy(aut1)
    aux.q_f = aut1.states + aut2.q_f
    aux.states = aux.states + aut2.states

    if aut1.q_f in aux.transitions:
        if '' in aux.transitions[aut1.q_f]:
            aux.transitions[aut1.q_f][''].append(aut1.states)
        else:
            aux.transitions[aut1.q_f][''] = [aut1.states]
    else:
        aux.transitions[aut1.q_f] = {}
        aux.transitions[aut1.q_f][''] = [aut1.states]

    for i in aut2.transitions.keys():
        for j in aut2.transitions[i].keys():
            c = [d + aut1.states for d in aut2.transitions[i][j]]
            if (i + aut1.states) in aux.transitions:
                if j in aux.transitions[i + aut1.states]:
                    aux.transitions[i + aut1.states][j].extend(c)
                else:
                    aux.transitions[i + aut1.states][j] = c
            else:
                aux.transitions[i + aut1.states] = {}
                aux.transitions[i + aut1.states][j] = c
    return aux

def incognit(aut1):
    aux = copy.deepcopy(aut1)

    if aut1.q_0 in aux.transitions:
        if '' in aux.transitions[aut1.q_0]:
            aux.transitions[aut1.q_0][''].append(aux.q_f)
        else:
            aux.transitions[aut1.q_0][''] = [aux.q_f]
    else:
        aux.transitions[aut1.q_0] = {}
        aux.transitions[aut1.q_0][''] = [aux.q_f]

    return aux

def Kleen_star(aut1):
    aux = copy.deepcopy(aut1)

    if aux.q_f in aux.transitions:
        if '' in aux.transitions[aux.q_f]:
            aux.transitions[aut1.q_f][''].append(aux.q_0)
        else:
            aux.transitions[aut1.q_f][''] = [aux.q_0]
    else:
        aux.transitions[aut1.q_f] = {}
        aux.transitions[aut1.q_f][''] = [aux.q_0]

def epsilon_closure(aut1, states):

    aux = copy.deepcopy(states)

    for s in aux:
        if s in aut1.transitions:
            for i in aut1.transitions[s]:
                if i == '':
                    for a in aut1.transitions[s][i]:
                        if a in aux:
                            continue
                        aux.append(a)
    return set(aux)

def to_deterministic(aut1):
    states = [epsilon_closure(aut1, [aut1.q_0])]

    transitions = {}
    final_states = set()

    count = 0
    while count < len(states):
        aux = {}

        for state in states[count]:
            if not state in aut1.transitions:
                continue
            for symbol in aut1.transitions[state].keys():
                if symbol == '':
                    continue

                if symbol in aux:
                    aux[symbol].update(aut1.transitions[state][symbol])
                else:
                    aux[symbol] = set()
                    aux[symbol].update(aut1.transitions[state][symbol])
        
        for item in aux:
            closure = epsilon_closure(aut1, list(aux[item]))
            c = indice(states, closure)
            if c != -1:
                k = c
            else:
                k = len(states)
                states.append(closure)
            if count in transitions:
                transitions[count][item] = k
            else:
                transitions[count] = {}
                transitions[count][item] = k
        if aut1.q_f in states[count]:
            final_states.add(count)
        count += 1
    return states, transitions, final_states

def range_(aut1, aut2):
    aux = Nfa()
    a = list(aut1.transitions.keys())[0]
    z = list(aut2.transitions.keys())[0]
    character = [chr(i) for i in range(ord(a), ord(z) + 1)]
    aux.transitions[aux.q_0] = {}
    for s in character:
        aux.transitions[aux.q_0][s] = [aux.q_f]
    return aux

def indice(state, item):
    for a in range(len(state)):
        if state[a] == item:
            return a
    return -1

def character(ch):
    new = Nfa()
    new.transitions[new.q_0] = {}
    new.transitions[new.q_0][ch] = [new.q_f]
    return new

def build_lexer(aut1):
    states, transitions, final_states = to_deterministic(aut1)

    def check(code):
        c = 0 
        read = 0
        for i in range(len(code)):
            if code[i] in transitions[c][code[1]]:
                c = transitions[c][code[i]]
                read = i
            else:
                break

        return c in final_states, read
    return check
e = character('a')
a = Nfa(0, 5, 6, {0 : {'a': [1, 3], 'b': [3, 4], '': [1]}, 1 : {'a': [2], '': [2, 5]}, 2:{'b': [3,2]}})

character = [chr(i) for i in range(ord('a'), ord('z') + 1)]
print(character)