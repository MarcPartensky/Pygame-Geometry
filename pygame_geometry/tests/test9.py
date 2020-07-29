import random
import numpy as np

alphabet="abcdefghijklmnopqrstuvwxyz"
n=len(alphabet)
d=dict(zip(range(n),alphabet))
print(d.keys())
print(d.values())

rr=random.randint

a=np.array([(rr(0,10),rr(0,10)) for i in range(10)])
print(list(set(a.reshape(2*len(a)))))


A = {'10':1, '11':1, '12':1, '10':2, '11':2, '11':3}
B = {'11':1, '11':2}
#a=all(map( A.pop, B))
C = {k:v for k,v in A.items() if k not in B}
print(C)
