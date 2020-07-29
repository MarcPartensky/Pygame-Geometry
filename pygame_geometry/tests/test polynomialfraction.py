from marclib.polynomial import Polynomial,RationalFunction
from mynewgrapher import Grapher
from mycontext import Context
from sympy import init_printing, Symbol, expand
init_printing()

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')

if __name__=="__main__":
    p1=Polynomial([0,6,1,6,5])
    q1=Polynomial([0,5,2,1,-2])
    f1=RationalFunction(p1,q1)

    p2=Polynomial([0,5,2,1,-2])
    q2=Polynomial([0,6,1,6,5])
    f2=RationalFunction(p2,q2)

    p3=Polynomial([a,b])
    q3=Polynomial([c,d])
    f3=RationalFunction(p3,q3)
    print(f3)

    f=f1+f2

    print(f.poles)

    context=Context()
    g=Grapher(context,[f1,f2,f])
    g()
