from .force import Force
from .motion import Motion
from .abstract import Point,Segment,Vector
from .curves import Trajectory
from .material import Material
from .step import Step
from . import colors
from . import force

import math
import copy

digits=2

class MaterialPoint(Material,Point):
    """Point that obbey to the laws of physics."""

    #Group operations
    def null(n=3,d=2):
        """Return the neutral material point."""
        return MaterialPoint(Motion.null(n=n,d=d))

    def sum(points,d=2):
        """Return the sum of the material points."""
        result=MaterialPoint.null(d=d)
        for point in points:
            result+=point
        return result

    def average(points):
        """Return the average of the material points."""
        return MaterialPoint.sum(points)/len(points)

    mean=average
    neutral=zero=null

    #Creating material points
    def random(corners=[-1,-1,1,1],**kwargs):
        """Create a random material point using optional minimum and maximum."""
        motion=Motion.random(corners)
        return MaterialPoint(motion,**kwargs)

    def createFromAbstract(point,n=3,d=2):
        """Create a material point from a Point instance."""
        motion=Motion(Vector(point),n=n,d=d) #Initializing a motion instance
        return MaterialPoint(motion) #Initializing a material point instance

    #Initializing the material point
    def __init__(self,motion=Motion.null(),mass=1,color=colors.WHITE):
        """Create a material point."""
        self.motion=motion
        self.mass=mass
        self.color=color

    #String representation
    def __str__(self):
        """Return the string representation of a point."""
        x,y=self.getPosition()
        x,y=round(x,digits),round(y,digits)
        return "mp("+str(x)+","+str(y)+")"

    #Trajectory
    def getTrajectory(self,t=1,split=1,**kwargs):
        """Return the trajectory of the point supposing it is not under any
        extern forces or restraints."""
        points=[]
        for i in range(split):
            point=self.getNext(t)
            points.append(point)
        return Trajectory(points,**kwargs)

    def getSegment(self,t=1,**kwargs):
        """Return the direction made of the actual point and the future one."""
        p1=self.abstract
        p2=self.getNext(t).abstract
        return Segment(p1,p2,**kwargs)

    def getVector(self,t=1,**kwargs):
        """Return the vector made of the actual point and the future one."""
        p1=self.abstract
        p2=self.getNext(t).abstract
        return Vector.createFromTwoPoints(p1,p2,**kwargs)

    #Step (The step is the vector of the actual position to the next position.)
    def getStep(self):
        """Return the step of the material point."""
        return Step(self.abstract,self.getNext(1).abstract)

    def setStep(self,step):
        """Set the velocity of the form so the next step is the given one."""
        self.velocity=Vector.createFromTwoPoints(*step)

    def delStep(self):
        """Delete the step null by making the motion null."""
        self.velocity.setNull()
        self.acceleration.setNull()

    #Next
    def getNext(self,t=1):
        """Return the future point."""
        p=copy.deepcopy(self)
        p.update(t)
        return p

    def getNextPosition(self,t):
        """Return the next position of the object supposing there is no collisions."""
        self.motion.update(t)
        return self.position

    def getNextVelocity(self,t):
        """Return the next velocity of the object supposing there is no collisions."""
        self.motion.update(t)
        return self.getVelocity()

    #Show
    def show(self,window,**kwargs):
        """Show the material point on the window."""
        self.abstract.show(window,**kwargs)

    def showMotion(self,context):
        """Show the motion of a material point on the window."""
        self.velocity.show(context,self.abstract)
        self.acceleration.show(context,self.abstract)

    def showStep(self,context):
        """Show the step of the material point."""
        self.step.show(context)

    def showText(self,*args,**kwargs):
        """Show the text on the screen."""
        self.abstract.showText(*args,**kwargs)

    def showName(self,context):
        """Show the str representation of the object."""
        self.abstract.showText(context,str(self),color=self.color)

    def showAll(self,context):
        """Show all components of the material point that can be shown."""
        self.show(context)
        self.showStep(context)
        self.showMotion(context)
        self.showName(context)

    #Update
    def update(self,t=1):
        """Update the motion of the material point."""
        self.motion.update(t)

    def rotate(self,angle=math.pi,center=Point.origin()):
        """Rotate the point using an angle and the point of rotation."""
        self.abstract.rotate(angle,center)
        point=self.abstract
        point.rotate(angle,center)
        vector=Vector.createFromPoint(point)
        self.motion.setPosition(vector)

    #Iterate the components of the point
    def __iter__(self):
        """Iterate the position."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point through an iteration."""
        if self.iterator < 2:
            if self.iterator==0: value=self.motion.getPosition()[0]
            if self.iterator==1: value=self.motion.getPosition()[1]
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def __getitem__(self,index):
        """Return position components value using given index."""
        return self.position[index]

    def __setitem__(self,index,value):
        """Change position components value using given index and value."""
        self.position[index]=value

    #Abstract
    def getAbstract(self):
        """Return the abstract point that correspond to the point."""
        return Point(self.motion.position.components)

    def setAbstract(self,point):
        """Set the abstract point that correspond to the point."""
        self.motion.position.components=point.components

    def delAbstract(self):
        """Set the point the zero."""
        self.points=[]

    #Components
    def getComponents(self):
        """Return the components of the material point."""
        return self.abstract.components

    def setComponents(self,components):
        """Set the components of the material point to the given components."""
        self.abstract.components=components

    def delComponents(self):
        """Set the components of the material point to null."""
        self.abstract.components=[0 for i in range(len(self.abstract.components))]

    abstract=property(getAbstract,setAbstract,delAbstract,"Representation of the point as an abstract point.")
    components=property(getComponents,setComponents,delComponents,"Representation of the components of the material point.")
    step=property(getStep,setStep,delStep,"Representation of the step of the material point.")


FallingPoint=lambda :MaterialPoint()

if __name__=="__main__":
    from .surface import Surface
    surface=Surface(name="Material Point Test")
    points=[MaterialPoint.random(color=colors.darken(colors.YELLOW)) for i in range(5)]
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        for point in points:
            #point.showText(surface,point)
            point.update(t=0.001)
            t=point.getTrajectory(1,3,point_color=colors.darken(colors.RED))
            #point.show(surface,color=colors.RED,mode="cross")
            #point.showMotion(surface)
            point.showAll(surface)
            t.show(surface)
        surface.flip()
