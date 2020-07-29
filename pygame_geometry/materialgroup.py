from .materialform import MaterialForm
from .materialpoint import MaterialPoint
from .abstract import Vector,Segment,Line
from .motion import Motion
from . import colors

import itertools
import math

class MaterialCollider:
    """Class made especially to deal with one to one collisions."""
    def __init__(self):
        """Create a collider."""
        pass

    def set(self,object1,object2):
        """Set the objects of the collider."""
        self.object1=object1
        self.object2=object2

    def collide(self):
        """Deal with the collisions of two objects."""


    def getCollisionInstant(self):
        """Return the instant of the collision of two objects."""
        bt=1
        #steps=itertools.combinations(itertoolself.object1.steps,self.object2.steps)
        allsteps=[(s1,s2) for s1 in self.object1.steps for s2 in self.object2.steps]
        points=[self.isColliding(steps) for steps in allsteps]
        allsteps=itertools.compress(allsteps,points)
        instants=list(map(self.getInstant,allsteps))
        return min(instants+[1])

    def isColliding(self,steps):
        """Determine is the steps are colliding."""
        return steps[0].crossSegment(steps[1]) is not None

    def getInstant(self,steps):
        """Return the minimum of the instant of the point to the begining of the segments."""
        st1=steps[0]
        st2=steps[1]
        p=st1.crossSegment(st2)
        t1=Segment(st1.p1,p).length/st1.length
        t2=Segment(st1.p2,p).length/st2.length
        return min(t1,t2)


    def getCollisionPoints(self):
        """Return the points of collisions of the steps of the two objects."""
        points=[]
        for step1 in self.object1.steps:
            for step2 in self.object2.steps:
                point=step1.crossSegment(step2)
                if point:
                    points.append(point)
        return points


    def __call__(self,object1,object2):
        """Deal with the collisions of two objects."""
        pass
        return [object1,object2]

    def contact(self,object1,object2):
        """Determine if the two objects are actually in contact or not."""
        return object1.abstract|object2.abstract != []

class MaterialGroup:
    """Class used to manipulate groups of material objects together."""
    def __init__(self,*objects,collider=MaterialCollider()):
        """Create a material group with the list of objects."""
        self.objects=objects
        self.collider=collider

    def show(self,context):
        """Show all the objects on screen."""
        for object in self.objects:
            object.center.showMotion(context)
            object.show(context)

        l=len(self.objects)
        for i in range(l):
            for j in range(i+1,l):
                points=self.objects[i].abstract|self.objects[j].abstract
                if points!=[]:
                    self.objects[i].velocity*=0
                    print(points)
                    l1=Segment(*points[:2])
                    l1.color=colors.GREEN
                    l1.show(context)
                    p=l1.center
                    p.show(context,mode="cross",color=colors.RED)
                    c1=self.objects[i].center.abstract
                    v=Vector.createFromTwoPoints(c1,p)
                    v.color=colors.GREEN
                    v.show(context,c1)
                    v.norm=1
                    v.color=colors.BLUE
                    v.show(context,p)
                    v.showText(context,p,'up')
                    v.rotate(math.pi/2)
                    v.show(context,p)
                    v.showText(context,p,'uo')




    def showAll(self,context):
        """Show all the components of all the objects."""
        for object in self.objects:
            object.showAll(context)
        points=self.objects[0].abstract.crossForm(self.objects[1].abstract)
        for point in points:
            point.show(context,mode="cross",width=2,size=[0.02,0.02],color=colors.RED)


    def update(self,dt=1):
        """Update all the objects together accounting for their collisions."""
        for object in self.objects:
            object.update(dt)

    def getCollisionInstant(self,dt=1):
        """Return precisely the time of the first collision between all objects."""
        bt=1
        l=len(self.objects)
        for i in range(l):
            for j in range(1,l):
                self.collider.set(self.objects[i],self.objects[j])
                t=self.collider.getCollisionInstant()
                if t<bt:
                    bt=t
        return t

    def directUpdate(self,dt=1):
        """Update all the objects without accounting for their collisions."""
        for object in self.objects:
            object.update(dt)

    def collideWithGroup(self,group):
        """Deal with the collisions of the object of the group with another group."""
        pass

if __name__=="__main__":
    from .surface import Context
    context=Context(name="Material Group Test",fullscreen=True)
    f1=MaterialForm.random(corners=[-10,-10,10,10])
    f1.motion=Motion(Vector(0,20),Vector(0,-5,0),Vector(0,-1))
    f2=MaterialForm.random(corners=[-10,-10,10,10])
    #f2.fill=True
    f2.motion=Motion.null()
    g=MaterialGroup(f1,f2)
    t=g.getCollisionInstant(1)
    print(t)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        g.update(dt=0.01)
        g.show(context)
        context.flip()
