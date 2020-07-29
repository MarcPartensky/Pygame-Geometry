from myabstract import Line,Point
import math

l=Line(Point(1,0),math.pi/2)
print(l.point,l.angle)
print(l.angle==-math.pi/2)
p=Point.random()
print(p)
i=l.projectPoint(p)
print(i)
