from AST import *
from defaultCode import *
import copy

class Type_Code:
    def __init__(self):
        self.id_ = ''
        self.arguments = []
        self.atributes = []
        self.methods = []

class Code_Gen:
    def __init__(self):
        self.count = 0
        self.a = default
        self.globalVar = {}
        self.clases = {}
        self.arib = {}
        self.flag = 0

    def _NodeProgram(self, node: NodeProgram):
        for stat in node.stat_list:
            if isinstance(stat, NodeFunction):
                self.functionDeclaration(stat) 
        change = True
        while change:
            change = False
            for stat in node.stat_list:
                if isinstance(stat, NodeFunction) or isinstance(stat, NodeProtocol):
                    continue
                if isinstance(stat.IdA, NodePro_func):
                    type_id = stat.IdA.id_
                else:
                    type_id = stat.IdA.lex
                if type_id in self.clases:
                    continue
                if len(stat.inher) > 0 and stat.inher[0].lex not in self.clases:
                    continue
                stat.gener(self)
                change = True

        for stat in node.stat_list:
            if isinstance(stat, NodeType):
                continue
            stat.gener(self)
        expression = node.expression.gener(self)
        return self.a + '\n int main(int argc, char **argv){\n' + expression + ';\n}'
    
    def functionDeclaration(self, node: NodeFunction):
        code = '\n' + node.type_ + ' ' + node.id_ + '('
        for arg in node.arguments:
            code = code + arg.type_ + ' ' + arg.id_ + ', '
        if len(node.arguments) > 0:
            code = code[:-2]
        code = code + ');\n'
        self.a = self.a + code

    @staticmethod
    def _NodeNum(node: NodeNum):
        return 'Num(' + str(node.value) + ')'
    
    @staticmethod
    def _NodeStr(node: NodeStr):
        return 'String("' + node.value + '")'
    
    @staticmethod
    def _NodeBool(node: NodeBool):
        if node.value:
            return 'Num(1)'
        else:
            return 'Num(0)'

    def _NodePlus(self, node: NodePlus):
        return 'Sum(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeMinus(self, node: NodeMinus):
        return 'Minus(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeStar(self, node: NodeStar):
        return 'Mult(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeDiv(self, node: NodeDiv):
        return 'Division(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodePow(self, node: NodePow):
        return 'Pow(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeConcat_s(self, node: NodeConcat_s):
        if node.left.ret == 'double*' and node.right.ret == 'double*':
            return 'ConcatSdd(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
        if node.left.ret == 'double*' and node.right.ret == 'char*':
            return 'ConcatSdc(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
        if node.left.ret == 'char*' and node.right.ret == 'double*':
            'ConcatScd(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'

        return 'ConcatScc(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeConcat_d(self, node: NodeConcat_d):
        if node.left.ret == 'double*' and node.right.ret == 'double*':
            return 'ConcatScd(ConcatSdc(' + node.left.gener(self) + ', " "), ' + node.right.gener(self) + ')'
        if node.left.ret == 'double*' and node.right.ret == 'char*':
            return 'ConcatScc(ConcatSdc(' + node.left.gener(self) + ', " "), ' + node.right.gener(self) + ')'
        if node.left.ret == 'char*' and node.right.ret == 'double*':
            return 'ConcatScd(ConcatScc(' + node.left.gener(self) + ', " "), ' + node.right.gener(self) + ')'
        
        return 'ConcatScc(ConcatScc(' + node.left.gener(self) + ', " "), ' + node.right.gener(self) + ')'
    
    def _NodeAnd(self, node: NodeAnd):
        return 'And(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeOr(self, node: NodeOr):
        return 'Or(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeLess(self, node: NodeLess):
        return 'Less(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeLess_E(self, node: NodeLess_E):
        return 'LessE(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeGreater(self, node: NodeGreater):
        return 'Greater(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeGreater_E(self, node: NodeGreater_E):
        return 'GreaterE(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeEqual(self, node: NodeEqual):
        return 'Equal(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeDistint(self, node: NodeDistint):
        return 'Distint(' + node.left.gener(self) + ', ' + node.right.gener(self) + ')'
    
    def _NodeUnary_Minus(self, node: NodeUnary_Minus):
        return 'Num(-*' + node.op.gener(self) + ')'
    
    def _NodeUnary_Not(self, node: NodeUnary_Not):
        return 'Num(!*' + node.op.gener(self) + ')'
    
    def _NodeLetExpression(self, node: NodeLetExpression):
        local = copy.deepcopy(self.globalVar)
        cop = {}
        dev = node.ret
        name = self.count
        self.count = self.count + 1
        code = '\n' + dev + ' let' + str(name) + '('
        for key in self.globalVar:
            ret, value = self.globalVar[key]
            code = code + ret + ' ' + key + ', '
        
        if len(self.globalVar) > 0:
            code = code[:-2]
        code = code + '){\n'
        for asig in node.assignment_list:
            dev, key, value = asig.gener(self)
            self.globalVar[key] = (dev, value)
            cop[key] = (dev, value)
            c = dev[:-1]
            code = code + dev + ' ' + key + ' = malloc(sizeof(' + c + '));\n*' + key + ' = *' + value + ';\n'
        code = code + dev + ' result = malloc(sizeof(' + dev[:-1] + '));\n'
        code = code + node.expression.gener(self) + ';'
        x = code.rfind('\n')
        t = '*result = *'
        code = f"{code[:x+ 1]}{t}{code[x+1:]}" + '\nreturn result;\n}'
        #self.a = self.a[:2293] + code + self.a[2293:]
        self.a = self.a + code + '\n'
        p = 'let' + str(name) + '('
        for key in self.globalVar:
            if key not in cop:
                p = p + key + ', '
        if len(self.globalVar) - len(cop) > 0:
            p = p[:-2]
        p = p + ')'
        self.globalVar = local
        return p



    def _NodeAsign(self, node: NodeAsign):
        dev = node.IdT.type_
        key = node.IdT.gener(self)
        value = node.expression.gener(self)
        return dev, key, value
    
    def _NodeBlockExpression(self, node: NodeBlockExpression):
        d = ''
        for expr in node.list_:
            d = d + '\n' +  expr.gener(self) + ';'
        d = d[:-1]
        return d
    
    def _NodeIdT(self, node: NodeIdT):
        return  node.id_
    
    def _NodeAcces(self, node: NodeAcces):
        if not node.previous:
            if self.flag == 1 and node.id_ in self.arib:
                return self.arib[node.id_]
            return node.id_
        else:
            return node.previous.gener(self) + '->' + node.id_
    
    def _NodeDestAssigment(self, node: NodeDestAssigment):
        IdT = node.IdT.gener(self)
        expression = node.expression.gener(self)
        name = self.count
        self.count = self.count + 1
        self.globalVar[IdT] = (node.ret, expression)
        code = '\n' + node.ret + ' dest' + str(name) + '('
        for key in self.globalVar:
            #if key != IdT:
            ret, value = self.globalVar[key]
            code = code + ret + ' ' + key + ', '
        if len(self.globalVar) > 0:
            code = code[:-2]
        code = code + '){\n*' + IdT + ' = *' + expression + ';\nreturn ' + IdT + ';\n}'
        self.a = self.a + code

        p = 'dest' + str(name) + '('
        for key in self.globalVar:
            #if key != IdT:
            p = p + key + ', '
        if len(self.globalVar) > 0:
            p = p[:-2]
        p = p + ')'
        return p

    def _NodeWhile(self, node: NodeWhile):
        expression = node.expression.gener(self)
        block = node.block.gener(self)
        name = self.count
        self.count = self.count + 1
        code = '\n' + node.ret + ' while' + str(name) + '('
        for key in self.globalVar:
            ret, value = self.globalVar[key]
            code = code + ret + ' ' + key + ', '

        if len(self.globalVar) > 0:
            code = code[:-2]
        code = code + '){\n' + node.ret + ' result = malloc(sizeof(' + node.ret[:-1] + '));\nwhile(*' + expression + '){\n' + block + ';'
        x = code.rfind('\n')
        t = '*result = *'
        code = f"{code[:x+ 1]}{t}{code[x+1:]}" + '\n}\nreturn result;\n}'
        self.a = self.a + code + '\n'

        p = 'while' + str(name) + '('
        for key in self.globalVar:
            p = p + key + ', '
        if len(self.globalVar) > 0:
            p = p[:-2]
        p = p + ')'
        return p

    def _NodeCondition(self, node: NodeCondition):

        expression = node.expression.gener(self)
        do_ = node.do_.gener(self)
        else_ = node.else_.gener(self)
        name = self.count
        self.count = self.count + 1
        code = '\n' + node.ret + ' condition' + str(name) + '('
        for key in self.globalVar:
            ret, value = self.globalVar[key]
            code = code + ret + ' ' + key + ', '

        if len(self.globalVar) > 0:
            code = code[:-2]

        code = code + '){\n' + node.ret + ' result = malloc(sizeof(' + node.ret[:-1] + '));\nif(*' + expression + '){\n' + do_ + ';'
        x = code.rfind('\n')
        t = '*result = *'
        code = f"{code[:x+ 1]}{t}{code[x+1:]}" + '\n}\nelse{\n' + else_ + ';'
        x = code.rfind('\n')
        code = f"{code[:x+ 1]}{t}{code[x+1:]}" + '\n}\nreturn result;\n}'
        self.a = self.a + code + '\n'
        p = 'condition' + str(name) + '('
        for key in self.globalVar:
            p = p + key + ', '
        if len(self.globalVar) > 0:
            p = p[:-2]
        p = p + ')'
        return p
    
    def _NodeFunction(self, node: NodeFunction):
        code = '\n' + node.type_ + ' ' + node.id_ + '('
        for arg in node.arguments:
            code = code + arg.type_ + ' ' + arg.id_ + ', '
        if len(node.arguments) > 0:
            code = code[:-2]
        code = code + '){\n' + node.type_ + ' result = malloc(sizeof(' + node.type_[:-1] + '));\n' + node.funcblock.gener(self) + ';'
        x = code.rfind('\n')
        t = '*result = *'
        code = f"{code[:x+ 1]}{t}{code[x+1:]}" + '\nreturn result;\n}'
        self.a = self.a + code + '\n'
    
    def _NodeCallExpression(self, node: NodeCallExpression):
        id_ = node.IdT.gener(self)
        arguments = []
        for arg in node.arguments:
            arguments.append(arg.gener(self))
        if id_ == 'sin':
            return 'sin1(' + arguments[0] + ')'

        if id_ == 'cos':
            return 'cos1(' + arguments[0] + ')'

        if id_ == 'tan':
            return 'tan1(' + arguments[0] + ')'

        if id_ == 'sqrt':
            return 'sqrt1(' + arguments[0] + ')'

        if id_ == 'print':
            if arguments[0].ret == 'double*':
                return 'printf("%lf\n", ' + arguments[0] + ')'
            return 'printf(' + arguments[0] + ')'
        code = id_ + '('
        for arg in arguments:
            code = code + arg + ', '
        if len(arguments) > 0:
            code = code[:-2]
        return code + ')'
    
    def _NodeType(self, node: NodeType):
        if isinstance(node.IdA, NodePro_func):
            id_ = node.IdA.id_
        else:
            id_ = node.IdA.lex
        argumentos = []
        atributos = []
        metodos = []
        inher = None
        if len(node.inher) > 0:
            inher = node.inher[0].lex
        if inher != None and inher in self.clases:
            if len(node.inher) > 1:
                for i,arg in enumerate(node.inher):
                    if i == 0:
                        continue
                    if isinstance(arg, NodeIdT):
                        if (arg.id_, arg.type_) not in argumentos:
                            #argumentos.append((arg.id_, arg.type_))
                            4
                    else:
                        4#argumentos.append((arg.gener(self), self.clases[inher].arguments[i - 1][1]))
                        self.arib[self.clases[inher].arguments[i - 1][0]] = arg.gener(self)
            else:
                #argumentos.append((arg.id_, arg.type_))
                4
            print(self.arib)
            argumentos = copy.deepcopy(self.clases[inher].arguments)
            atributos = copy.deepcopy(self.clases[inher].atributes)
            metodos = copy.deepcopy(self.clases[inher].methods)
        code = '\ntypedef struct ' + id_ + '{\n'
        self.flag = 1
        values = []
        for atr in atributos:
            dev, key, value = atr.gener(self)
            values.append(value)
            code = code + '    ' + dev + ' ' + key + ';\n'
        self.flag = 0
        for atr in node.typeblock:
            if isinstance(atr, NodeAsign):

                dev, key, value = atr.gener(self)
                code = code + '    ' + dev + ' ' + key + ';\n'
                values.append(value)
                atributos.append(atr)
        
        self.flag = 0
        code = code + '}' + id_ + ';\n' + id_ + '* init' + id_ + '('
        if isinstance(node.IdA, NodePro_func):

            for arg in node.IdA.arguments:
                if (arg.id_, arg.type_) not in argumentos:
                    argumentos.append((arg.id_, arg.type_))
        for arg in argumentos:
            code = code + arg[1] + ' ' + arg[0] + ', '
        if len(argumentos) > 0:
            code = code[:-2]
        code = code + '){\n' + id_ + '* result = malloc(sizeof(' + id_ + '));\n'
        for i,atr in enumerate(atributos):
            dev, key, value = atr.gener(self)
            code = code + 'result->' + key + ' = ' + values[i] + ';\n'
        code = code + 'return result;\n}'
        self.a = self.a + code
        tip = Type_Code()
        tip.arguments = argumentos
        tip.atributes = atributos
        tip.methods = metodos
        tip.id_ = id_
        self.clases[id_] = tip
    
#print(default[2293:] + '\n{aaaaa')