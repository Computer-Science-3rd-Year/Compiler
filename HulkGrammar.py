from Grammar import *
from AST import *
G = Grammar()

Program = G.NonTerminal('Program', True)

Stat_list, Expression, Stat, def_func, def_type, def_protocol, arg_list, TypeA, FuncBlock, IdT, BlockExpression, IdA, Inher, TypeBlock, BaseType, CallExpression, atrib_list, asig, Ext, rule_list, BoolExpression, Predicate, ArithExpr, TypeTestExpr,  Termino, UnarySub, Factor, PrimitiveExpression, VectorLiteral, Acces, LetExpression, DestAsig, CondExpr, WhileExpr, ForExpr, DownExpr, TypeInst, expr_list, asig_list, OptionalCondition, Iterator, arg, File, TopLevel, Prototype, Members, ProtocolBlock, StructuredExpression, BasicExpression, S= G.NonTerminals('Stat_list Expression Stat def_func def_type def_protocol arg_list TypeA FuncBlock IdT BlockExpression IdA Inher TypeBlock BaseType CallExpression atrib_list asig Ext rule_list BoolExpression Predicate ArithExpr TypeTestExpr Termino UnarySub Factor PrimitiveExpression VectorLiteral Acces LetExpression DestAsig CondExpr WhileExpr ForExpr DownExpr TypeInst expr_list asig_list OptionalCondition Iterator arg File TopLevel Prototype Members ProtocolBlock StructuredExpression BasicExpression S')

function, Id, flecha, punto_c, type_, inherits, llave_a, llave_c, opar, cpar, protocol, extends, and_, or_, not_, menor, menor_e, mayor, mayor_e, equal, distinto, plus, minus, arroba, arroba_d, star, div, resto, pow_, num, str_, bool_, coma, let, in_ , asignar, asignar_d, if_, elif_, else_, while_, for_, is_, as_, dos_p, new_ , colchete_a, colchete_c, doble_or, punto = G.Terminals('function Id => ; type inherits { } ( ) protocol extends & | ! < <= > >= == != + - @ @@ * / % ^ num str bool , let in = := if elif else while for is as : new_ [ ] || .')

S %= Program, lambda s: s[1], None 
Program %= Stat_list + Expression + punto_c, lambda s: NodeProgram(s[1], s[2]), None, None, None

Stat_list %= Stat_list + Stat, lambda s: [*s[1], s[2]], None, None
Stat_list %= G.Epsilon, lambda s: []

Stat %= def_func, lambda s: s[1], None
Stat %= def_type, lambda s: s[1], None
Stat %= def_protocol, lambda s: s[1], None

def_func %= function + Id + opar + arg_list + cpar + TypeA + FuncBlock, lambda s: NodeFunction(s[2], s[4], s[6], s[7]), None, None, None, None, None, None, None

arg_list %= arg_list + coma + IdT, lambda s: [*s[1], s[3]], None, None, None
arg_list %= IdT, lambda s: [s[1]], None
arg_list %= G.Epsilon, lambda s: []

IdT %= Id + TypeA, lambda s: NodeIdT(s[1], s[2]), None, None
IdT %= Id, lambda s: NodeIdT(s[1], None), None

TypeA %= dos_p + Id, lambda s: s[1], None, None

FuncBlock %= BlockExpression, lambda s: s[0], None
FuncBlock %= flecha + Expression + punto_c, lambda s: s[2], None, None, None

def_type %= type_ + IdA + Inher + TypeBlock, lambda s: NodeType(s[2], s[3], s[4]), None, None, None, None

IdA %= Id + opar + arg_list + cpar, lambda s: [s[1], *s[3]], None, None, None, None
IdA %= Id, lambda s: [s[1]], None

Inher %= inherits + Id, lambda s: s[2], None, None
Inher %= G.Epsilon, lambda s: None

#BaseType %= Id, None, None
#BaseType %= CallExpression, None, None

TypeBlock %= llave_a + atrib_list + llave_c, lambda s: s[2], None, None, None

atrib_list %= atrib_list + asig, lambda s: [*s[1], s[2]], None, None
atrib_list %= atrib_list + Id + opar + arg_list + cpar + TypeA + FuncBlock, lambda s: [*s[1], NodeFunction(s[2], s[4], s[5], s[6])], None, None, None, None, None, None, None
atrib_list %= G.Epsilon, lambda s: []

def_protocol %= protocol + Id + Ext + llave_a + rule_list + llave_c, lambda s: NodeProtocol(s[2], s[3], s[5]), None, None, None, None, None, None

Ext %= extends + Id, lambda s:s[2], None, None
Ext %= G.Epsilon, lambda s: None

asig %= IdT + asignar + Expression + punto_c, lambda s: NodeAsign(s[1], s[3]), None, None, None, None

rule_list %= rule_list + Id + opar + arg_list + cpar + TypeA + punto_c, lambda s: [*s[1], NodePro_func(s[2], s[4], s[6])], None, None, None, None, None, None, None
rule_list %= G.Epsilon, lambda s: []

Expression %= BasicExpression, lambda s: s[1], None
Expression %= StructuredExpression, lambda s: s[1], None

BasicExpression %= Expression + and_ + BoolExpression, lambda s: NodeAnd(s[1], s[3]), None, None, None
BasicExpression %= Expression + or_ + BoolExpression, lambda s: NodeOr(s[1], s[3]), None, None, None
BasicExpression %= BoolExpression, lambda s: s[1], None

BoolExpression %= not_ + BoolExpression, lambda s: NodeUnary_Not(s[2]), None, None
BoolExpression %= Predicate, lambda s: s[1], None

Predicate %= ArithExpr + menor + ArithExpr, lambda s: NodeLess(s[1], s[3]), None, None, None
Predicate %= ArithExpr + menor_e + ArithExpr, lambda s: NodeLess_E(s[1], s[3]), None, None, None
Predicate %= ArithExpr + mayor + ArithExpr, lambda s: NodeGreater(s[1], s[3]), None, None, None
Predicate %= ArithExpr + mayor_e + ArithExpr, lambda s: NodeGreater_E(s[1], s[3]), None, None, None
Predicate %= ArithExpr + equal + ArithExpr, lambda s: NodeEqual(s[1], s[3]), None, None, None
Predicate %= ArithExpr + distinto + ArithExpr, lambda s: NodeDistint(s[1], s[3]), None, None, None
Predicate %= TypeTestExpr, lambda s: s[1], None
Predicate %= ArithExpr, lambda s: s[1], None

ArithExpr %= ArithExpr + plus + Termino, lambda s: NodePlus(s[1], s[3]), None, None, None
ArithExpr %= ArithExpr + minus + Termino, lambda s: NodeMinus(s[1], s[3]), None, None, None
ArithExpr %= ArithExpr + arroba + Termino, lambda s: NodeConcat_s(s[1], s[3]), None, None, None
ArithExpr %= ArithExpr + arroba_d + Termino, lambda s: NodeConcat_d(s[1], s[3]), None, None, None
ArithExpr %= Termino, lambda s: s[1], None

Termino %= Termino + star + UnarySub, lambda s: NodeStar(s[1], s[3]), None, None, None
Termino %= Termino + div + UnarySub, lambda s: NodeDiv(s[1], s[3]), None, None, None
Termino %= Termino + resto + UnarySub, lambda s: NodeResto(s[1], s[3]), None, None, None
Termino %= UnarySub, lambda s: s[1], None

UnarySub %= minus + Factor, lambda s: NodeUnary_Minus(s[2]), None, None
UnarySub %= Factor, lambda s: s[1], None

Factor %= PrimitiveExpression + pow_ + Factor, lambda s: NodePow(s[1], s[3]), None, None, None
Factor %= PrimitiveExpression, lambda s: s[1], None

StructuredExpression %= BlockExpression, lambda s: s[1], None
StructuredExpression %= LetExpression, lambda s: s[1], None
StructuredExpression %= DestAsig, lambda s: s[1], None
StructuredExpression %= CondExpr, lambda s: s[1], None
StructuredExpression %= WhileExpr, lambda s: s[1], None
StructuredExpression %= ForExpr, lambda s: s[1], None
StructuredExpression %= DownExpr, lambda s: s[1], None


PrimitiveExpression %= opar + Expression + cpar, lambda s: s[2], None, None, None
PrimitiveExpression %= num, lambda s: NodeNum(s[1]), None
PrimitiveExpression %= str_, lambda s: NodeStr(s[1]), None
PrimitiveExpression %= bool_, lambda s: NodeBool(s[1]), None
PrimitiveExpression %= VectorLiteral, lambda s: s[1] , None
PrimitiveExpression %= CallExpression, lambda s: s[1], None
PrimitiveExpression %= Acces, lambda s: s[1], None
PrimitiveExpression %= BlockExpression, lambda s: s[1], None
#PrimitiveExpression %= BlockExpression, None, None
#PrimitiveExpression %= LetExpression, None, None
#PrimitiveExpression %= DestAsig, None, None
#PrimitiveExpression %= CondExpr, None, None
#PrimitiveExpression %= WhileExpr, None, None
#PrimitiveExpression %= ForExpr, None, None
#PrimitiveExpression %= DownExpr, None, None
PrimitiveExpression %= TypeInst, lambda s: s[1], None

BlockExpression %= llave_a + expr_list + llave_c, lambda s: NodeBlockExpression(s[2]), None, None, None
expr_list %= expr_list + Expression + punto_c, lambda s: [*s[1], s[2]], None, None, None
expr_list %= G.Epsilon, lambda s: []

LetExpression %= let + asig_list + in_ + Expression, lambda s: NodeLetExpression(s[2], s[4]), None, None, None, None
asig_list %= asig_list + IdT + asignar + Expression + coma, lambda s: [*s[1], NodeDestAssigment(s[2], s[4])], None, None, None, None, None
asig_list %= IdT + asignar + Expression, lambda s: DestAsig(s[1], s[3]), None, None, None

DestAsig %= Acces + asignar_d + Expression, lambda s: NodeDestAssigment(s[1], s[3]), None, None, None

CondExpr %= if_ + opar + Expression + cpar + Expression + OptionalCondition, lambda s: NodeCondition(s[3], s[5], s[6]), None, None, None, None, None, None

OptionalCondition %= elif_ + opar + Expression + cpar + Expression + OptionalCondition, lambda s: NodeCondition(s[3], s[5], s[6]), None, None, None, None, None, None
OptionalCondition %= else_ + Expression, lambda s: s[2], None, None

WhileExpr %= while_ + opar + Expression + cpar + Expression, lambda s: NodeWhile(s[3], s[5]), None, None, None, None, None

ForExpr %= for_ + opar + Iterator + cpar + Expression, lambda s: NodeFor(s[3], s[5]), None, None, None, None, None

Iterator %= IdT + in_ + Expression, lambda s: NodeIterator(s[1], s[3]), None, None, None

TypeTestExpr %= ArithExpr + is_ + Id, lambda s: NodeTypeTestExpr(s[1], s[3]), None, None, None

DownExpr %= PrimitiveExpression + as_ + Id, lambda s: NodeDownExpression(s[1], s[3]), None, None, None

TypeInst %= new_ + Id + opar + arg + cpar, lambda s: NodeTypeInst(s[2], s[4]), None, None, None, None, None

arg %= arg + coma + Expression, lambda s: [*s[1], s[2]], None, None, None
arg %= Expression, lambda s: [s[1]], None
arg %= G.Epsilon, lambda s: []

VectorLiteral %= colchete_a + arg + colchete_c, lambda s: NodeVectorL(s[2]), None, None, None
VectorLiteral %= colchete_a + Expression + doble_or + Iterator + colchete_c, lambda s: NodeVector_C(s[2], s[4]), None, None, None, None, None

CallExpression %= Acces + opar + arg + cpar, lambda s: NodeCallExpression(s[1], s[3]), None, None, None, None

Acces %= Acces + punto + Id, lambda s: NodeAcces(s[3], s[1]), None, None, None
Acces %= Acces + colchete_a + Expression + colchete_c, lambda s: NodeIndex(s[1], s[3]), None, None, None, None
Acces %= Id, lambda s: NodeAcces(s[1], None), None

