from AST import *
from Context import *
import math
import random
from importlib import import_module
from lexer import Token
import sys
import copy

#class Error:
#    pass
global_scope = Context({
    'E': math.e,
    'PI': math.pi,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'exp': math.exp,
    'log': math.log,
    'rand': random.random,
    'print': print,
    'import': import_module,
    'Number': float,
    'String': str,
    'Object': object,
    #'range': range
})

tipos = {
    type(4.5): 'double*',
    type(4): 'double*',
    type("cadena"): 'char*',
    type(None): 'void',
    type(True): 'double*',
    'Number': 'double*',
    'String': 'double*',
    'dynamic': 'void*',
    type(Error()): 'Error'
}
valores ={
    'Number': 4.0,
    'String': 'cadena'
}
#errors = []
compiler = False

class Function:
    def __init__(self, id_, type_, arguments, funcblock, ejecute):
        self.id_ = id_
        if type_ != None and type(type_) != str:
            self.type_ = type_.lex
        else:
            self.type_ = None
        self.arguments = arguments
        self.funcblock = funcblock
        self.ejecute = ejecute#############runtime
        self.closure = ejecute.context
    
    def __call__(self, *args, **kwargs):
        scope = self.ejecute.context
        self.ejecute.context = Context(father=self.closure)

        ids = []

        for argument in self.arguments:
            ids.append(argument.check(self.ejecute))
        if len(ids) != len(args):
            raise Exception(f'Cantidad de argumentos invalida en la funcion: \'{self.id_}\', esperada: \'{len(ids)}\', pasada: \'{len(args)}\'')
        for i in range(0, len(args)):
            self.ejecute.context[ids[i]] = args[i]

        if '#super' in self.closure.general:
            if self.id_ in self.closure['#super'].attrs.general:
                self.ejecute.context.check_key('base', self.closure['#super'].attrs[self.id_])
        aux = self.funcblock.check(self.ejecute)
        self.ejecute.context = scope
        return aux 

    def rev(self):
        ids = []
        scope = self.ejecute.context
        self.ejecute.context = Context(father = self.closure)
        for argument in self.arguments:
            ids.append(argument.check(self.ejecute))

        for i in range(0, len(self.arguments)):
            self.ejecute.context[ids[i]] = 'dinamic'
        
        if '#super' in self.closure.general:
            if self.id_ in self.closure['#super'].attrs.general:
                self.ejecute.context.check_key('base', self.closure['#super'].attrs[self.id_])
        aux = self.funcblock.check(self.ejecute)
        for i, arg in enumerate(self.arguments):
            if arg.type_ == None:
                if isinstance(self.ejecute.context.general[ids[i]], Objectbase):
                    arg.type_ = tipos[self.ejecute.context.general[ids[i]].type_id]
                else:
                    if type(self.ejecute.context.general[ids[i]]) == type('srg') and self.ejecute.context.general[ids[i]][-1] == '*':
                        arg.type_ = self.ejecute.context.general[ids[i]]
                    else:
                        arg.type_ = tipos[type(self.ejecute.context.general[ids[i]])]
            else:
                if isinstance(arg.type_, str) and arg.type_[:-1] == '*':
                    arg.type_ = arg.type_
                else:
                    try:
                        arg.type_ = tipos[arg.type_.lex]
                    except:
                        4
        self.ejecute.context = scope
        return aux
class Type:
    def __init__(self, ejecute, IdA, inher, typeblock):
        self.IdA = IdA
        self.inher = inher
        self.typeblock = typeblock
        self.ejecute = ejecute
        self.supertype = None
        self.super_args = []

        if isinstance(IdA, NodePro_func):
            self.type_id = IdA.id_
        else:
            self.type_id = IdA.lex
        
        if len(inher) > 0:
            if len(inher) == 1:
                self.supertype = self.ejecute.context[inher[0].lex]
            else:
                self.supertype = self.ejecute.context[inher[0].lex]
                self.super_args = inher[1:]
            if isinstance(self.supertype.IdA, NodePro_func):
                if len(self.supertype.IdA.arguments) != len(self.super_args):
                    if not isinstance(self.IdA, NodePro_func):
                        self.IdA = NodePro_func(IdA, [], None)
                    t = []
                    for i in self.supertype.IdA.arguments:
                        t.append(copy.deepcopy(i))
                    self.IdA.arguments = t + self.IdA.arguments
    def __call__(self, *args, **kwargs):

        scope = self.ejecute.context
        self.ejecute.context = Context(father = self.ejecute.context)

        if isinstance(self.IdA, NodePro_func):
            ids = []
            for arg in self.IdA.arguments:
                ids.append(arg.check(self.ejecute))
    
            for i in range(len(args)):
                if args[i] == None:
                    self.ejecute.context[ids[i]] = global_scope[self.IdA.arguments[i].type_.lex]
                else:
                    self.ejecute.context[ids[i]] = args[i]
            self.ejecute.context = Context(father = self.ejecute.context)
        if self.supertype:
            a = []
            for i in self.super_args:
                a.append(i.check(self.ejecute))
            
            basetype = self.supertype(*a)
            self.ejecute.context = Context(father = basetype.attrs)
            self.ejecute.context.check_key('#super', basetype)
        inst = Objectbase(self.ejecute.context, self)
        self.ejecute.context.check_key('self', inst)
        for atrib in self.typeblock:
            atrib.check(self.ejecute)
        self.ejecute.context = scope

        return inst
    def rev(self):
        scope = self.ejecute.context
        self.ejecute.context = Context(father = self.ejecute.context)

        if isinstance(self.IdA, NodePro_func):
            ids = []
            for arg in self.IdA.arguments:
                ids.append(arg.check(self.ejecute))
    
            for i in range(len(self.IdA.arguments)):
                if self.IdA.arguments[i].type_ != None:
                    self.ejecute.context[ids[i]] = valores[self.IdA.arguments[i].type_.lex]
                else:
                    self.ejecute.context[ids[i]] = 'dinamic'
            self.ejecute.context = Context(father = self.ejecute.context)
        if self.supertype:
            a = []
            for i in self.super_args:
                a.append(i.check(self.ejecute))
            basetype = self.supertype(*a)
            self.ejecute.context = Context(father = basetype.attrs)
            self.ejecute.context.check_key('#super', basetype)
        inst = Objectbase(self.ejecute.context, self)
        self.ejecute.context.check_key('self', inst)
        for atrib in self.typeblock:
            atrib.check(self.ejecute)
            if isinstance(atrib, NodeFunction):
                aux = self.ejecute.context[atrib.id_].rev()
                if isinstance(aux, Objectbase):
                    atrib.type_ = tipos[aux.type_.type_id]
                else:
                    atrib.type_ = tipos[type(aux)]
        if isinstance(self.IdA, NodePro_func):
            for i, arg in enumerate(self.IdA.arguments):
                if arg.type_ == None:
                    if isinstance(self.ejecute.context.father[ids[i]], Objectbase):
                        arg.type_ = tipos[self.ejecute.context.father[ids[i]].type_id]
                    else:
                        if type(self.ejecute.context.father[ids[i]]) == type('srg') and self.ejecute.context.father[ids[i]][-1] == '*':
                            arg.type_ = self.ejecute.context.father[ids[i]]
                        else:
                            arg.type_ = tipos[type(self.ejecute.context.father[ids[i]])]
                else:
                    if isinstance(arg.type_, str) and arg.type_[:-1] == '*':
                        arg.type_ = arg.type_
                    else:
                        try:
                            arg.type_ = tipos[arg.type_.lex]
                        except:
                           4
        self.ejecute.context = scope
        tipos[self.type_id] = str(self.type_id)
        return inst
    def __instancecheck__(self, instance):
        return self.__subclasscheck__(instance.type_)

    def __subclasscheck__(self, subclass):
        return subclass is self or self.__subclasscheck__(subclass.supertype)

class Protocol:
    def __init__(self, ejecute, rule_list, supertype):
        self.ejecute = ejecute
        self.rule_list = rule_list
        self.supertype = supertype

    def __instancecheck__(self, inst):
        for name, return_type, param_types in self.rule_list:
            if name not in inst.attrs.general:
                return False
            m = inst.attrs[name]
            if not isinstance(m, Function):
                return False
            res = self.ejecute.context[return_type.lex] if return_type else object
            met_res_type = self.ejecute.context[m.type_] if m.type_ \
                else object
            if not issubclass(met_res_type, res):
                return False

            if len(param_types) != len(m.arguments):
                return False
            met_arg_t = [arg.type_ for arg in m.arguments]
    
            for i in range(len(param_types)):
                res_param_t = self.ejecute.context[param_types[i].lex] if param_types[i] else object
                met_resol_param_type = self.ejecute.context[met_arg_t[i].lex] if met_arg_t[i] \
                    else object

                if not issubclass(res_param_t, met_resol_param_type):
                    return False
        if self.supertype:
            supertype = self.ejecute.context[self.supertype.lex]
            return supertype.__instancecheck__(inst)

        return True

class Objectbase:
    def __init__(self, attrs, type_):
        self.attrs = attrs
        self.type_ = type_

    def __getitem__(self, item):
        return self.attrs['__getitem__'](item)

    def __setitem__(self, key, value):
        return self.attrs['__setitem__'](key, value)

    def __call__(self, *args, **kwargs):
        return self.attrs['__call__'](*args, **kwargs)
class Ejecute:
    def __init__(self, context):
        self.context = context
        self.bandera = False
    def _NodeProgram(self, node: NodeProgram):
        change = True
        mask = []
        for i in node.stat_list:
            mask.append(False)
        while change:
            change = False
            for i, stat in enumerate(node.stat_list):
                if isinstance(stat, NodeFunction):
                    continue
                if isinstance(stat, NodeProtocol):
                    continue
                if isinstance(stat.IdA, NodePro_func):
                    type_id = stat.IdA.id_
                else:
                    type_id = stat.IdA.lex
                if type_id in self.context.general:
                    continue
                if len(stat.inher) > 0 and stat.inher[0].lex not in self.context.general:
                    continue
                stat.check(self)
                mask[i] = True
                change = True

        
        for i, stat in enumerate(node.stat_list):
            if isinstance(stat, NodeType):
                if isinstance(stat.IdA, NodePro_func):
                    type_id = stat.IdA.id_
                else:
                    type_id = stat.IdA.lex
                if type_id in self.context.general and mask[i] == False:
                    errors.append(f'El tipo:  \'{type_id}\', ya fue definido, error at line: {stat.token.line}, column: {stat.token.column}')
                    compiler = True
                    continue
                if type_id not in self.context.general and len(stat.inher) > 0:
                    errors.append(f'Error al heredar del tipo:  \'{stat.inher[0].lex}\', ya fue definido, error at line: {stat.token.line}, column: {stat.token.column}')
                    compiler = True
                    continue
                continue
            stat.check(self)
        self.bandera = True
        for stat in node.stat_list:
            if isinstance(stat, NodeProtocol):
                continue
            if isinstance(stat, NodeFunction):
                aux = self.context[stat.id_].rev()
                if isinstance(aux, Objectbase):
                    stat.type_ = tipos[aux.type_.type_id]
                else:
                    stat.type_ = tipos[type(aux)]
            if isinstance(stat, NodeType):
                if isinstance(stat.IdA, NodePro_func):
                    self.context[stat.IdA.id_].rev()
                else:
                    self.context[stat.IdA.lex].rev()
        self.bandera = False   
        aux = node.expression.check(self)
        if len(errors) > 0:
            for i in errors:
                print(i)
            sys.exit()
        return aux
    
    def _NodeFunction(self, node: NodeFunction):
        id_ = node.id_
        arguments = node.arguments
        self.context.check_key(id_, Function(id_, node.type_, arguments, node.funcblock, self))

    def _NodePro_func(self, node: NodePro_func):
        return node.id_, node.arguments
    
    def _NodeType(self, node: NodeType):
        type_ = Type(self, node.IdA, node.inher, node.typeblock)
        self.context.check_key(type_.type_id, type_)
        valores[type_.type_id] = type_
    
    def _NodeProtocol(self, node: NodeProtocol):
        rules = []
        for i in node.rule_list:
            id_, arguments = i.check(self)
            rules.append((id_, i.type_, [argument.type_ for argument in arguments]))

        protocol = Protocol(self, rules, node.extends)
        self.context.check_key(node.id_, protocol)
    @staticmethod
    def _NodeNum(node: NodeNum):
        return node.value
    
    @staticmethod
    def _NodeStr(node: NodeStr):
        return node.value
    
    @staticmethod
    def _NodeBool(node: NodeBool):
        return node.value
    
    def _NodeVectorL(self, node: NodeVectorL):
        return self.context['Vector']([elem.check(self) for elem in node.list_])

    def _NodePlus(self, node: NodePlus):
        #print(self.context.general)
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.right.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father
        left = node.left.check(self)
        right = node.right.check(self)
        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
            if f"La suma solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}" not in errors:
                errors.append(f"La suma solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        return float(left) + float(right)
    
    def _NodeMinus(self, node: NodeMinus):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father
        left = node.left.check(self)
        right = node.right.check(self)
    
        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
            errors.append(f"La resta solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        return  float(left) - float(right)

    def _NodeConcat_s(self, node: NodeConcat_s):
        left = node.left.check(self)
        try:
            a = str(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"No se puede concatenar, error at line: {node.token.line}, column {node.token.column}, Mi no es casteable a str")
            compiler = True
            return Error()
        right = node.right.check(self)
        try:
            b = str(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"No se puede concatenar, error at line: {node.token.line}, column {node.token.column}, Md no es casteable a str")
            compiler = True
            return Error()
        return str(a) + str(b)
    
    def _NodeConcat_d(self, node: NodeConcat_d):
        left = node.left.check(self)
        try:
            a = str(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"No se puede concatenar, error at line: {node.token.line}, column {node.token.column}, Mi no es casteable a str")
            compiler = True
            return Error()
        right = node.right.check(self)
        try:
            b = str(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"No se puede concatenar, error at line: {node.token.line}, column {node.token.column}, Md no es casteable a str")
            compiler = True
            return Error()
        return str(a) + ' ' + str(b)
    
    def _NodeStar(self, node: NodeStar):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father

        left = node.left.check(self)
        right = node.right.check(self)
        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
            errors.append(f"La multiplicación solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()

        return float(left) * float(right)

    def _NodeDiv(self, node: NodeDiv):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father
        left = node.left.check(self)
        right = node.right.check(self)
        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
            errors.append(f"La división solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        return float(left) / float(right)
    
    def _NodeResto(self, node: NodeResto):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father
        left = node.left.check(self)
        right = node.right.check(self)
        
        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
            errors.append(f"El resto solo esta definido para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        return float(left) % float(right)
    
    def _NodePow(self, node: NodePow):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = .0
                    break
                d = d.father
        left = node.left.check(self)
        right = node.right.check(self)

        if (type(left) != float and type(left) != int) or (type(right) != float and type(right) != int) :
            if type(left) == Error or type(right) == Error:
                return Error() 
    
            errors.append(f"La potencia solo esta definida para los numeros, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        return float(left) ** float(right)
    
    def _NodeAnd(self, node: NodeAnd):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = True
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = True
                    break
                d = d.father
        left = node.left.check(self)
        try:
            a = bool(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es bool, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)
        try:
            b = bool(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es bool, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
            
        return a and b
    
    def _NodeOr(self, node: NodeOr):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = True
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = True
                    break
                d = d.father
        left = node.left.check(self)
        try:
            a = bool(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es bool, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)   
        try:
            b = bool(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es bool, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
            
        return a or b
    
    def _NodeUnary_Minus(self, node: NodeUnary_Minus):
        if isinstance(node.op, NodeAcces) and self.context[node.op.id_] == 'dinamic':
            d = self.context
            while d:
                if node.op.id_ in d.general:
                    d.general[node.op.id_] = 4.0
                    break
                d = d.father
    
        op = node.op.check(self)
        if type(op) != float and type(op) != int:
            if type(op) == Error:
                return Error()
            errors.append(f'El operador de resta solo es aplicable a numeros, error at line: {node.token.line}, column: {node.token.column}')
            compiler = True
            return Error()
        return - float(op)
    def _NodeUnary_Not(self, node: NodeUnary_Not):
        if isinstance(node.op, NodeAcces) and self.context[node.op.id_] == 'dinamic':
            d = self.context
            while d:
                if node.op.id_ in d.general:
                    d.general[node.op.id_] = 4.0
                    break
                d = d.father
        op1 = node.op.check(self)
        try:
           op =  bool(op1)
        except:
            if type(op1) == Error:
                return Error()
            errors.append(f'El operador not solo es aplicable a booleanos, error at line: {node.token.line}, column: {node.token.column}')
            compiler = True
            return Error()
        return not bool(op)

    def _NodeLess(self, node: NodeLess):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father
        left = node.left.check(self)
        try:
            a = float(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)    
        try:
            b = float(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
            
        return a < b

    def _NodeLess_E(self, node: NodeLess_E):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father

        left = node.left.check(self)
        try:
            a = float(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)    
        try:
            b = float(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        
        return a <= b
    def _NodeGreater(self, node: NodeGreater):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father

        left = node.left.check(self)
        try:
            a = float(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)    
        try:
            b = float(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        
        return a > b
    
    def _NodeGreater_E(self, node: NodeGreater_E):
        if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.left.id_] = 4.0
                    break
                d = d.father
        if isinstance(node.right, NodeAcces) and self.context[node.right.id_] == 'dinamic':
            d = self.context
            while d:
                if node.left.id_ in d.general:
                    d.general[node.right.id_] = 4.0
                    break
                d = d.father

        left = node.left.check(self)
        try:
            a = float(left)
        except:
            if type(left) == Error:
                return Error()
            errors.append(f"Mi no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        right = node.right.check(self)    
        try:
            b = float(right)
        except:
            if type(right) == Error:
                return Error()
            errors.append(f"Md no es number, error at line: {node.token.line}, column {node.token.column}")
            compiler = True
            return Error()
        
        return a >= b
    
    def _NodeEqual(self, node: NodeEqual):
        
        a = node.left.check(self)
        b = node.right.check(self)
        return a == b
    
    def _NodeDistint(self, node: NodeDistint):
        a = node.left.check(self)
        b = node.right.check(self)
        return a != b
    
    def _NodeWhile(self, node: NodeWhile):
        expression = node.expression.check(self)
        aux = 0
        while expression:
            if type(expression) != type(True) and type(expression) != type(1.0) and type(expression) != type(4):
                if type(expression) == Error:
                    return Error()
                errors.append(f"La expresion del while debe evaluar a bool, error at line: {node.token.line}, column {node.token.column}")
                compiler = True
                return Error()    
            if node.ret == None and type(node.block.check(self)) in tipos:
                node.ret = tipos[type(node.block.check(self))]
            aux = node.block.check(self)
            expression = node.expression.check(self)
        return aux
    def _NodeCondition(self, node: NodeCondition):
        
        a = node.expression.check(self)
        b = node.do_.check(self)
        c = node.else_.check(self)
        if type(a) != type(True) and type(a) != type(1.0) and type(a) != type(4):
                if type(a) == Error:
                    return Error()
                errors.append(f"La expresion de una condicional debe evaluar a bool, error at line: {node.token.line}, column {node.token.column}")
            
        if type(a) == Error or type(b) == Error or type(c) == Error:
            return Error()
        if a:
            node.ret = tipos[type(b)]
            return b
        else:
            node.ret = tipos[type(c)]
            return c
    
    def _NodeBlockExpression(self, node: NodeBlockExpression):
        result = None
        for expr in node.list_:
            result = expr.check(self)
        #if node.ret == None and type(result) in self.tipos:
        #        node.ret = self.tipos[type(result)]
        return result
    
    def _NodeLetExpression(self, node: NodeLetExpression):
        scope = self.context

        for assig in node.assignment_list:
            self.context = Context(father = self.context)
            assig.check(self)
        
        aux = node.expression.check(self)
        self.context = scope
        if type(aux) == Error:
            return Error()
        if node.ret == None:
            node.ret = tipos[type(aux)]
        
        return aux
    
    def _NodeIterator(self, node: NodeIterator):
        return node.IdT.check(self), node.expression.check(self)
    
    def _NodeFor(self, node: NodeFor):
        name, iterator = node.iterator.check(self)
        IdT = f'#iter{id(node)}'

        cond = NodeCallExpression(NodeAcces(Token(-1, -1, str, 'next'),
                                           NodeAcces(Token(-1, -1, str, IdT), None)), [])

        block = NodeLetExpression([
            NodeAsign(NodeIdT(Token(-1, -1, str, name), None),
                          NodeCallExpression(NodeAcces(Token(-1, -1, str, 'current'),
                                                      NodeAcces(Token(-1, -1, str, IdT))), []))],
            node.block)
        aux = None

        self.context = Context(father=self.context)
        self.context.check_key(IdT, iterator)
        
        while cond.check(self):
            aux = block.check(self)
            if type(aux) == Error:
                return Error()

        self.context = self.context.father
        return aux

    def _NodeVector_C(self, node: NodeVector_C):
        vector = []

        name, iterator = node.iterator.check(self)
        IdT = f'#iter{id(node)}'

        cond = NodeCallExpression(NodeAcces(Token(-1, -1, str, 'next'),
                                           NodeAcces(Token(-1, -1, str, IdT), None)), [])

        block = NodeLetExpression([
            NodeAsign(NodeIdT(Token(-1, -1, str, name), None),
                          NodeCallExpression(NodeAcces(Token(-1, -1, str, 'current'),
                                                      NodeAcces(Token(-1, -1, str, IdT))), []))],
            node.expression)

        self.context = Context(father=self.context)
        self.context.check_key(IdT, iterator)
        while cond.check(self):
            vector.append(block.check(self))
        self.context = self.context.father
        return self.context['Vector'](vector)

    def _NodeAsign(self, node: NodeAsign):
        
        key = node.IdT.check(self)
        value = node.expression.check(self)
        if node.IdT.type_ != None:
            if type(node.IdT.type_) != str:
                node.IdT.type_ = tipos[node.IdT.type_.lex]
        else:
            if isinstance(value, Objectbase):
                node.IdT.type_ = tipos[str(value.type_.type_id)]
            else:
                try:
                    node.IdT.type_ = tipos[type(value)]
                except:
                    4
        node.ret = node.IdT.type_
        self.context.check_key(key, value)
    def _NodeIdT(self, node: NodeIdT):
        return node.id_
    
    def _NodeAcces(self, node: NodeAcces):
        if not node.previous:
            if type(self.context[node.id_]) == type(Error()):
                errors[-1] = f"Invalid Key: {node.id_} at line : {node.token.line}, column {node.token.column}"
                return Error()
            return self.context[node.id_]

        previous = node.previous.check(self)
        if isinstance(previous, Objectbase):
            return previous.attrs[node.id_]
        return getattr(previous, node.id_)
    
    def _NodeIndex(self, node: NodeIndex):
        i = int(node.expression.check(self))
        a = node.IdT.check(self)
        return a[i]

    def _NodeCallExpression(self, node: NodeCallExpression):
        call = node.IdT.check(self)
        t = []

        #if isinstance(node.left, NodeAcces) and self.context[node.left.id_] == 'dinamic':
        #    d = self.context
        #    while d:
        #        if node.left.id_ in d.general:
        #            d.general[node.left.id_] = 4.0
        #            break
        #        d = d.father
        for i, arg in enumerate(node.arguments):
            z = arg.check(self)
            t.append(z)
            if isinstance(arg, NodeAcces) and self.context[arg.id_] == 'dinamic':
                d = self.context
                while d:
                    if arg.id_ in d.general:
                        if call == math.sin or call == math.cos or call == math.sqrt or call == math.tan or call == print:
                            d.general[arg.id_] = 4.0
                        else:
                            if call.arguments[i].type_ == None:
                                call.rev()
                            d.general[arg.id_] = call.arguments[i].type_
                        break
                    d = d.father
            if type(t[-1]) == Error:
                return Error()
        if self.bandera:
            if hasattr(call, 'id_'):
                if self.context.rev(call.id_ + '#@') == 'None':
                    if call.type_ == 'Number':
                        return 4.0
                    if call.type_ == 'String':
                        return 'concat'
                    #print(call.id_)
                    return 4
            if hasattr(call, 'id_'):
                self.context[call.id_ + '#@'] = 4
            if node.IdT.id_ == 'range':
                return call(*[int(arg.check(self)) for arg in node.arguments])
            if node.IdT.id_ == 'print':
                return None
            if node.IdT.id_ == 'sin' or node.IdT.id_ == 'cos' or node.IdT.id_ == 'sqrt':
                return 4
        
        return call(*t)

    def _NodeTypeInst(self, node: NodeTypeInst):
        type_ = self.context[node.type_.lex]
        t = []
        for arg in node.arguments:
            t.append(arg.check(self))
            if type(t[-1]) == Error:
                return Error
        a = type_(*t)
        return a
    
    def _NodeDestAssigment(self, node: NodeDestAssigment):
        IdT = node.IdT
        value = node.expression.check(self)

        if isinstance(IdT, NodeIndex):
            i = IdT.expression.check(self)
            vec = IdT.IdT.check(self)
            vec[i] = value
        elif not IdT.previous:
            self.context[IdT.id_] = value
        else:
            prev = IdT.previous.check(self)
            if isinstance(prev, Objectbase):
                prev.attrs[IdT.id_] = value
            else:
                setattr(prev, IdT.id_, value)
        node.ret = tipos[type(value)]
        return value
    
    def _NodeDownExpression(self, node: NodeDownExpression):
        return node.expression.check(self)
    
    def _NodeTypeTestExpr(self, node: NodeTypeTestExpr):
        return isinstance(node.expression.check(self), self.context[node.type_.lex])

default_runtime = Ejecute(global_scope)
