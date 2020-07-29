from .materialpoint import MaterialPoint
from .abstract import Form,Point,Vector
from .material import Material
from .motion import Motion
from .force import Force

from . import materialpoint
from . import force
from . import colors
import math
import copy

class MaterialForm(Material,Form):
    """A material form is a form that is composed of material points and act
    according to them only by linking them. However, it's not really useful in
    practice because manipulating the material points directly is not an easy
    task."""

    def null():
        """Return the null material form."""
        return MaterialForm([],[])

    def random(corners=[-1,-1,1,1],n=5):
        """Create a random material form."""
        form=Form.random(corners,n=n)
        return MaterialForm.createFromForm(form)

    def createFromForm(form):
        """Create a material form using a Form instance."""
        return MaterialForm([MaterialPoint.createFromAbstract(point) for point in form.points])

    def __init__(self,points,fill=False,point_mode=0,point_radius=0.01,point_width=2,side_width=1,point_color=colors.WHITE,side_color=colors.WHITE,area_color=colors.WHITE):
        """Create a material form."""
        self.points=points
        self.fill=fill

        self.point_mode=point_mode
        self.point_radius=point_radius
        self.point_width=point_width

        self.area_color=area_color
        self.point_color=point_color

        self.side_width=side_width
        self.side_color=side_color

    def __str__(self):
        """Return the string representation of the material form."""
        return "mf("+",".join([str(p) for p in self.points])+")"

    #Abstract
    def getAbstract(self):
        """Return the object under a Form by conversion."""
        return Form([p.getAbstract() for p in self.points])

    def setAbstract(self,form):
        """Set the abstract representation of the material form to a form."""
        self.__dict__=MaterialForm.createFromForm(form).__dict__

    def delAbstract(self,form):
        """Set the abstract representation of the material form to null."""
        self.__dict__=MaterialFrom.null().__dict__


    def getCompleteForm(self,point_mode=None,point_radius=None,point_width=None,side_width=None,fill=None,area_color=None,point_color=None,side_color=None):
        """Return the object under a Form type by conversion."""
        if not point_mode: point_mode=self.point_mode
        if not point_radius: point_radius=self.point_radius
        if not point_width: point_width=self.point_width
        if not side_width: side_width=self.side_width
        if not fill: fill=self.fill
        if not area_color: area_color=self.area_color
        if not point_color: point_color=self.point_color
        if not side_color: side_color=self.side_color
        points=[point.abstract for point in self.points]
        return Form(points,fill=fill,
                    point_mode=point_mode,point_radius=point_radius,
                    point_width=point_width,side_width=side_width,
                    point_color=point_color,side_color=side_color,
                    area_color=area_color)

    def getPosition(self):
        """Return the position of the center of the material form."""
        return self.form.center.position

    def getAbstractPoints(self):
        """Return all the abstract points of the object."""
        return self.abstract.points


    #Next

    def getNext(self,dt):
        """Return the form after a duration dt."""
        points=[p.getNext(dt) for p in self.points]
        m=copy.deepcopy(self)
        m.points=points
        return m

    #Motion
    def getMotion(self):
        """Return the motion of the object."""
        return Motion.average([point.motion for point in self.points])

    def setMotion(self,nm):
        """Set the motion of the object."""
        m=self.getMotion()
        delta=nm-m
        for point in self.points:
            point.motion+=delta

    def delMotion(self):
        """Set the motion to null."""
        self.motion=Motion.null()

    def show(self,context):
        """Show the form on the context."""
        self.getCompleteForm().show(context)

    def showNext(self,context,dt=1):
        """Show the next form on the context."""
        self.getNext(dt).abstract.show(context)

    def showMotion(self,context):
        """Show the motion on a context."""
        self.motion.velocity.show(context,self.position)
        self.motion.acceleration.show(context,self.position)

    def showSteps(self,context):
        """Show the steps of the material form."""
        for point in self.points:
            point.showStep(context)

    def showAll(self,context):
        """Show all the components of the points of the material form."""
        self.getCompleteForm().show(context)
        self.center.showAll(context)
        for point in self.points:
            point.showAll(context)

    def update(self,t=1):
        """Update the form by updating all its points."""
        for point in self.points:
            point.update(t)

    def rotate(self,angle=math.pi,center=Point.origin()):
        """Rotate the form by rotating its points."""
        for point in self.points:
            point.rotate(angle,center)

    def getMass(self):
        """Calculate the mass of the form using its area and the mass of the material_points that define it."""
        """The way used to calculate it is arbitrary and should be improved."""
        mass=sum([point.getMass() for point in self.points])
        mass*=self.abstract.area
        return mass

    def __getitem__(self,index):
        """Return the material point of number 'index'."""
        return self.points[index]

    def __setitem__(self,index,point):
        """Return the material point of number 'index'."""
        self.points[index]=point

    def getCollisionInstant(self,other,dt=1):
        """Return the instant of the collision the material form with the other object."""

    def getPointSteps(self,dt=1):
        """Return the segments that correspond to the steps the points of the
        material form made during the time 'dt'."""
        return [p.getStep(dt) for p in self.points]

    def __or__(self,other):
        """Determine the points of intersections of the material point and another material object."""
        if isinstance(other,MaterialForm): return self.crossMaterialForm(other)

    def crossMaterialForm(self,other):
        """Return the material point of intersection between two material forms."""
        f1=self.abstract
        f2=other.abstract
        points=f1.crossForm(f2)
        return [MaterialPoint.createFromAbstract(point) for point in points]

    def getTrajectory(self,dt=1):
        """Return the segments that are defined by the trajectory of each point."""
        return [Segment(p.getPoint(dt),p.getNextPoint(dt)) for p in self.points]

    #Center
    def getCenter(self):
        """Return the material center of the form."""
        return MaterialPoint.average(self.points)

    def setCenter(self,nc):
        """Set the center of the material form."""
        ac=self.getCenter()
        v=Vector.createFromTwoPoints(nc,ac)
        for point in self.points:
            point+=v

    def delCenter(self):
        """Set the center to the origin."""
        self.setCenter(Point.origin())

    #Position
    def getPosition(self):
        """Return the position of the center of the material form."""
        v=Vector.average([point.position for point in self.points])
        v.color=colors.GREEN
        return v

    def setPosition(self,position):
        """Set the position of the material form to the given position."""
        self.setCenter(position)

    def delPosition(self):
        """Set the position of the material form to the origin."""
        self.setCenter(Point.origin())

    #Velocity
    def getVelocity(self):
        """Return the velocity of the center of the material form."""
        v=Vector.average([point.velocity for point in self.points])
        v.color=colors.BLUE
        return v

    def setVelocity(self,velocity):
        """Set the velocity of the center of the material form."""
        for point in self.points:
            point.velocity=velocity

    def delVelocity(self):
        """Set the velocity to the null vector."""
        self.setVelocity(Vector.null())

    #Acceleration
    def getAcceleration(self):
        """Return the acceleration of the material form."""
        v=Vector.average([point.acceleration for point in self.points])
        v.color=colors.RED
        return v

    def setAcceleration(self,acceleration):
        """Set the acceleration of the material form to the given acceleration."""
        for point in self.points:
            point.acceleration=acceleration

    def delAcceleration(self):
        """Set the acceleration to the null vector."""
        self.setAcceleration(Vector.null())

    #Steps
    def getSteps(self):
        """Return the steps of each material point of the material form."""
        return [point.step for point in self.points]

    def setSteps(self,steps):
        """Set the steps of the material points."""
        for i,point in enumerate(self.points):
            point.step=steps[i]

    def delSteps(self):
        """Set the steps of the material points to null."""
        for (i,point) in enumerate(self.points):
            point.step=Segment.null()

    center=property(getCenter,setCenter,"Representation of the material center of the form.")
    abstract=property(getAbstract,setAbstract,delAbstract,"Representation of the form in the abstract.")
    motion=property(getMotion,setMotion,delMotion,"Representation of the motion of the form.")
    position=property(getPosition,setPosition,delPosition,"Representation of the position of the form.")
    velocity=property(getVelocity,setVelocity,delVelocity,"Representation of the velocity of the form.")
    acceleration=property(getAcceleration,setAcceleration,delAcceleration,"Representation of the acceleration of the form.")
    #abstract_center=property(getAbstractCenter,setAbstractCenter,delAbstractCenter,"Representation of the abstract center of the material form.")
    #abstract_points=property(getAbstractPoints,setAbstractPoints,delAbstractPoints,"Representation of the abstract points of the material form.")
    steps=property(getSteps,setSteps,delSteps,"Representation of the steps of the material form.")



FallingForm=lambda:MaterialForm([materialpoint.FallingPoint() for i in range(5)])

if __name__=="__main__":
    from .context import Surface
    surface=Surface()
    c1=[-10,-10,10,10]
    f1=Form.random(c1,n=5)
    f1=MaterialForm.createFromForm(f1)
    f1.velocity=Vector(0,1)
    f1.acceleration=Vector(0,-0.01)
    print(f1)

    c2=[-10,-10,10,10]
    f2=Form.random(c2,n=5)
    f2=MaterialForm.createFromForm(f2)

    #print(form[0].forces)
    #print(form.getMass())
    origin=Point.origin()
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        f1.update(t=1)
        f2.update(t=1)
        f1.rotate(0.01,f1.center.abstract)
        f2.rotate(-0.01,f2.center.abstract)
        for p in f1|f2:
            p.show(surface)
        surface.draw.window.print("f1: "+str(f1.motion),(10,10))
        surface.draw.window.print("f2: "+str(f2.motion),(10,40))
        f1.show(surface)
        f2.show(surface)
        f1.showNext(surface)
        f2.showNext(surface)
        f1.showMotion(surface)
        f2.showMotion(surface)
        f1.showSteps(surface)
        f2.showSteps(surface)
        surface.flip()
