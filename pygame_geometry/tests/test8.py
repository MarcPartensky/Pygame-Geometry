from mymotion import Motion
from myabstract import Vector,Segment,Form

m=Motion.random(n=2)
print(m)

v=Vector.random(d=2)
print(v)
print(v.norm)

s=Segment.random(d=2)
print(s.length)


f=Form.random(n=5,d=2)
print(f)

print(dict(zip(range(10),range(10))))
