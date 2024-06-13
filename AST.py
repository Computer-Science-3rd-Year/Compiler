class Node:
    pass

class NodeProgram(Node):
    def __init__(self, stat_list, expression):
        self.stat_list = stat_list
        self.expression = expression

class NodeFunction(Node):
    def __init__(self, id_, arguments, type_, funcblock):
        self.id_ = id_
        self.arguments = arguments
        self.type_ = type_
        self.funcblock = funcblock

class NodeIdT(Node):
    def __init__(self, id_, type_):
        self.id_ = type_
        self.type_ = type_

class NodeType(Node):
    def __init__(self, IdA, inher, typeblock):
        self.IdA = IdA
        self.inher = inher
        self.typeblock = typeblock

class NodeAsign(Node):
    def __init__(self, IdT, expression):
        self.IdT = IdT
        self.expression = expression

class NodeProtocol(Node):
    def __init__(self, id_, extends, block):
        self.id_ = id_
        self.extends = extends
        self.block = block

class NodePro_func(Node):
    def __init__(self, id_, arguments, type_):
        self.id_ = id_
        self.arguments = arguments
        self.type_ = type_

class NodeBynary_Op(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class NodePlus(NodeBynary_Op):
    pass

class NodeMinus(NodeBynary_Op):
    pass

class NodeStar(NodeBynary_Op):
    pass

class NodeDiv(NodeBynary_Op):
    pass

class NodeResto(NodeBynary_Op):
    pass

class NodePow(NodeBynary_Op):
    pass

class NodeAnd(NodeBynary_Op):
    pass

class NodeOr(NodeBynary_Op):
    pass

class NodeLess(NodeBynary_Op):
    pass

class NodeLess_E(NodeBynary_Op):
    pass

class NodeGreater(NodeBynary_Op):
    pass

class NodeGreater_E(NodeBynary_Op):
    pass

class NodeEqual(NodeBynary_Op):
    pass

class NodeDistint(NodeBynary_Op):
    pass

class NodeConcat_s(NodeBynary_Op):
    pass

class NodeConcat_d(NodeBynary_Op):
    pass

class NodeUnary_Op(Node):
    def __init__(self, op):
        self.op = op

class NodeUnary_Minus(NodeUnary_Op):
    pass

class NodeUnary_Not(NodeBynary_Op):
    pass

class NodeAcces(Node):
    def __init__(self, id_, previous):
        self.id_ = id_
        self.previous = previous

class NodeNum(Node):
    def __init__(self, num):
        self.value = num.lex

class NodeStr(Node):
    def __init__(self, str_):
        self.value = str_.lex

class NodeBool(Node):
    def __init__(self, bool_):
        self.value = bool(bool_.lex)

class NodeList_Expression(Node):
    def __init__(self, list_):
        self.list_ = list_

class NodeBlockExpression(NodeList_Expression):
    pass

class NodeVectorL(NodeList_Expression):
    pass

class NodeLetExpression(Node):
    def __init__(self, assignment_list, expression):
        self. assignment_list = assignment_list
        self.expression = expression

class NodeDestAssigment(Node):
    def __init__(self, IdT, expression):
        self.IdT = IdT
        self.expression = expression

class NodeCondition(Node):
    def __init__(self, expression, do_, else_):
        self.expression = expression
        self.do_ = do_
        self.else_ = else_

class NodeWhile(Node):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

class NodeFor(Node):
    def __init__(self, iterator, block):
        self.iterator = iterator
        self.block = block

class NodeIterator(Node):
    def __init__(self, IdT, expression):
        self.IdT = IdT
        self.expression = expression

class NodeDownExpression(Node):
    def __init__(self, expression, type_):
        self.expression = expression
        self.type_ = type_

class NodeTypeInst(Node):
    def __init__(self, type_, arguments):
        self.type_ = type_
        self.arguments = arguments

class NodeCallExpression(Node):
    def __init__(self, IdT, arguments):
        self.IdT = IdT
        self.arguments = arguments

class NodeTypeTestExpr(Node):
    def __init__(self, expression, type_):
        self.expression = expression
        self.type_ = type_

class NodeVector_C(Node):
    def __init__(self, expression, iterator):
        self.expression = expression
        self.iterator = iterator

class NodeIndex(Node):
    def __init__(self, IdT, expression):
        self.IdT = IdT
        self.expression = expression
