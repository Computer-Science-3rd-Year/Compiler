#from Check_AST import *
from Check import *
from regex import *
from HulkGrammar import *
from Parser import *
from lexer import tokenizer



d = tokenizer('''
function tan(x: Number): Number => sin(x) / cos(x);
function cot(x) => 1 / tan(x);
function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
    function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
            
        };
protocol Hashable {
    hash(): Number;
}
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}
protocol Iterable {
    next() : Boolean;
    current() : Object;
}

type Range(min:Number, max:Number) {
    min = min;
    max = max;
    current = min - 1;

    next(): Boolean => (self.current := self.current + 1) < self.max;
    current(): Number => self.current;
}
function range(min, max) => new Range(min, max);
type Point(x,y) {
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
type Knight inherits Person {
    name() => "Sir" @@ base();
}

type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
    hash() : Number {
        5;
    }
}
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
type Superman {
}
type Bird {
}
type Plane {
}
type A {
    hello() => print("A");
}
type B inherits A {
    hello() => print("B");
}

type C inherits A {
    hello() => print("C");
}
{  
    let a = (let b = 6 in b * 7) in print(a);
    print(let b = 6 in b * 7);
    let a = 20 in {
        let a = 42 in print(a);
        print(a);
    };
    let a = 7, a = 7 * 6 in print(a);
    let a = 7 in
        let a = 7 * 6 in
            print(a);
    let a = 0 in {
        print(a);
        a := 1;
        print(a);
    };
    let a = 0 in
        let b = a := 1 in {
            print(a);
            print(b);
        };
    let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
    let a = 42 in print(if (a % 2 == 0) "even" else "odd");
    let a = 42 in
        if (a % 2 == 0) {
            print(a);
            print("Even");
        }
        else print("Odd");
    let a = 42, mod = a % 3 in 
        print(
            if (mod == 0) "Magic"
            elif (mod % 3 == 1) "Woke"
            else "Dumb"
        );
    
    let x = [x^2 || x in range(1,10)] in for (i in x) print(i);
};
              ''')
from CodeGen import *
parse = slr_parser(G, lambda x: x.type_)
derivation = parse(d)
#print(derivation.expression.assignment_list[0].expression)
derivation.check(default_runtime)


#print(derivation.expression.assignment_list[0].expression.len_)
#a = Code_Gen()
#print(derivation.gener(a))