from myabstract import Segment, Line, Point, Vector
from mymanager import Manager
import mycolors
import math

class Tester(Manager):
    def __init__(self):
        super().__init__()
        self.l1=Line(Point.null(),0)
        self.l2=Line.random(borns=[-10,10])
        self.intersection=None

    def show(self):
        self.l1.show(self.context)
        self.l2.show(self.context)
        if self.intersection:
            self.intersection.show(self.context)

    def update(self):
        v=Vector(*self.context.point())
        self.l1.angle=v.angle
        self.intersection=self.l1.crossLine(self.l2)
        if self.intersection:
            self.intersection.color=mycolors.RED
            self.intersection.radius=1

class Tester(Manager):
    def __init__(self):
        #super().__init__()
        #self.l=Line(Point.null(),math.pi/2+1e-1)
        self.s=Segment.createFromTuples((-1,0),(-1,1),color=mycolors.GREEN,width=2)
        print(self.s.angle==math.pi/2)
        print(self.s.line.angle,self.s.line.point)
        self.p=Point.null(color=mycolors.RED,fill=True)
        self.projection=None

    def show(self):
        self.s.getLine(color=mycolors.YELLOW).show(self.context)
        self.s.show(self.context)
        self.p.show(self.context)
        if self.projection:
            self.projection.show(self.context,mycolors.BLUE)

    def update(self):
        self.p.position=list(self.context.point())
        self.projection=self.s.line.projectPoint(self.p)
        if self.projection:
            self.projection.fill=True

t=Tester()
#t()
