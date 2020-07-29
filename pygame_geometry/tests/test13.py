from mymanager import Manager
from myabstract import Circle,Segment
from myrectangle import Rectangle
from mycontext import Context

import mycolors
import random
import math

def oldcrossSquareCircle(square,circle):
    """Determine if a square is crossing a circle."""
    p,s=square; c,r=circle
    px,py=p; cx,cy=c
    sg=Segment.createFromTuples(p,c)
    l=sg.length
    a=sg.angle
    #x=n*math.cos(a)
    #n=x/math.cos(a)
    if -math.pi/4<=abs(a)<3*math.pi/4:
        n=s/(2*math.sin(a))
    else:
        n=s/(2*math.cos(a))
    return l-r<n


def isCircleInSquare(square,circle):
    """Detect the collision of a square and a circle."""
    qx,qy,qr=square
    cx,cy,cr=circle
    return abs(qx-cx)<=qr/2-cr and abs(qy-cy)<=qr/2-cr

def isCircleCrossingSquare(square,circle):
    """Detect the collision of a square and a circle."""
    qx,qy,qr=square
    cx,cy,cr=circle
    return abs(qx-cx)<=qr/2+cr and abs(qy-cy)<=qr/2+cr

class Tester(Manager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        r=random.uniform(1,2)
        x=random.uniform(-1,1)
        y=random.uniform(-1,1)
        self.circle=Circle(x,y,radius=r)
        r=random.uniform(5,10)
        x=random.uniform(-1,1)
        y=random.uniform(-1,1)
        self.rectangle=Rectangle((x,y),(r,r))
        self.moving=False

    def reactMouseMotion(self,event):
        self.circle.position=list(self.context.point())
        c=(*self.circle.position,self.circle.radius)
        r=(*self.rectangle.position, min(self.rectangle.size))
        if isCircleInSquare(r,c):
            self.circle.border_color=mycolors.GREEN
            self.rectangle.side_color=mycolors.GREEN
        elif isCircleCrossingSquare(r,c):
            self.circle.border_color=mycolors.RED
            self.rectangle.side_color=mycolors.RED
        else:
            self.circle.border_color=mycolors.WHITE
            self.rectangle.side_color=mycolors.WHITE

    def show(self):
        self.circle.show(self.context)
        self.rectangle.show(self.context)




if __name__=="__main__":
    t=Tester()
    t()
