from mycontext import Context
import mycolors
import cmath
import random

cx=[0+50j,0+18j,12+0j,-14+0j]
cy=[-60-30j,0+8j,0-10j,0]

a=list(zip(cx,cy))
print(a)
context=Context()

n=100

l=[complex(random.uniform(-1,1),random.uniform(-1,1)) for i in range(n)]

while context.open:
    context.check()
    context.control()
    context.clear()
    context.show()
    for e in l:
        z=cmath.exp(complex(e))
        context.draw.complex(context.screen,mycolors.WHITE,z,0.1)
    context.flip()
