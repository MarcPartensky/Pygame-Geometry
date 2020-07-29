from myabstract import Form, Line

import math

#f = Form.createFromTuples([(0,1), (1,0), (1,1)])
f = Form.random(n=3)

v1, v2, v3 = f.vectors

# print(",".join(map(lambda x: str(x.angle), f.vectors)))
print([str(v.angle) for v in f.vectors])

a1 = (v2.angle - v1.angle) % math.pi
a2 = (v3.angle - v2.angle) % math.pi
a3 = (v1.angle - v3.angle) % math.pi

print("ai:", a1, a2, a3)

print("sum:", sum([a1, a2, a3])/math.pi)

# l = Line.random()
# print(l.angle)

print("f.angles:", f.angles)
print("sum(f.angles):", sum(f.angles))

print("f.abs_angles:", f.abs_angles)

print("sum(f.abs_angles):", sum(f.abs_angles))
\