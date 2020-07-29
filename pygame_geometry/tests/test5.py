from marclib.polynomial import Polynomial
from mygrapher import Grapher
from mywindow import Window
import functools
import math


prod=lambda l:functools.reduce(lambda a,b: a*b,l)

#p=Polynomial([2,1])
sample=lambda f,xmin,xmax,n:[f(xmin+(xmax-xmin)*i/n) for i in range(n)]
interpolator=lambda x,s:sum([s[j]*prod([(len(s)*x-i)/(j-i) for i in range(len(s)) if i!=j]) for j in range(len(s))])
s=sample(math.cos,-10,10,100)
print(s)
cosinus_interpolation=lambda x:interpolator(x,s)
print(cosinus_interpolation(0))
#print(sample(math.cos,-10,10,100))

window=Window(size=[1000,800],fullscreen=False)
fs=[math.cos,cosinus_interpolation]
grapher=Grapher(fs)
grapher(window)
