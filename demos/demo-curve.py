from pygame_geometry.context import Surface
from pygame_geometry.curves import Trajectory, BezierCurve
from pygame_geometry.abstract import Point
from pygame_geometry import colors

import random

# create objects
surface=Surface(name="Curves demonstration")
l=10
points=[Point(2*x,random.randint(-5,5)) for x in range(l)]
t=Trajectory(points,segment_color=colors.GREEN)
b=BezierCurve(points,segment_color=colors.RED)
n=0
ncp=50 #number construction points

while surface.open:
    # surface stuff
    surface.check()
    surface.clear()
    surface.control()
    surface.show() # show a math grid in background

    # update
    Point.turnPoints([1/1000 for i in range(l)],points)
    n=(n+1)%(ncp+1)
    b.showConstruction(surface,n/ncp)
    p1=b(n/ncp)
    p2=Point(*t(n/ncp))

    # show
    t.show(surface)
    b.show(surface)
    p1.show(surface,color=colors.YELLOW,radius=0.1,fill=True)
    p2.show(surface,color=colors.YELLOW,radius=0.1,fill=True)

    # flip
    surface.flip()
