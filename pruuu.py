#from Check_AST import *
from Check import *
from regex import *
from HulkGrammar import *
from Parser import *
from lexer import tokenizer

d = tokenizer('''
              
type Point(x, y) {
            x = x;
            y = y;
            getX() => self.x;
            getY() => self.y;

            setX(x) => self.x := x;
           setY(y) => self.y := y;
        }

        type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
            rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
        }

        let pt = new PolarPoint(PI/4, sqrt(2)) in
            print(pt.rho() @@ pt.getX());
''')
#d = tokenizer('''
#    type A(x,y){
#              x = x + 1;
#              y = y + 4;
#              get() => self.y;
#    }
#    type B(x,y, z) inherits A{
#              z = z + 4;
#    }
#              4;
#''')
d = tokenizer(
    '''
    type Vector(v) {
            v = v;
            index = -1;
            __getitem__ = self.v.__getitem__;

            size() => self.v.__len__();

            next() {
                self.index := self.index + 1;
                self.index < self.size()
            }

            current() => self.v[self.index];

        }

        let
            v = 4
        in{
            v:= 5;
            print(v ** 2)
            };
        '''
)

from CodeGen import *
parse = slr_parser(G, lambda x: x.type_)
derivation = parse(d)
derivation.check(default_runtime)


#print(derivation.stat_list[1].inher[1])
#a = Code_Gen()
#print(derivation.gener(a))
dic = {'Michel': 7.0, 'Marlon': 4.0}
del dic['Marlon']