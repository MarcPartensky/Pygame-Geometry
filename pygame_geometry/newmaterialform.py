from .materialpoint import MaterialPoint
from .abstract import Form,Point,Vector
from .motion import Motion
from .force import Force

from . import materialpoint
from . import force
from . import colors

import math


class MaterialForm(Form):
    def random(corners=[-1,-1,1,1],number=5):
        """Create a random material form."""
        points=[MaterialPoint.random(min,max) for n in range(number)]
        return MaterialForm(points)

    def createFromForm(form,forces=[]):
        """Create a material form using a Form instance."""
        material_points=[MaterialPoint.createFromPoint(point,forces) for point in form.getPoints()]
        return MaterialForm(material_points)

    def __init__(self,points,fill=False,point_mode=0,point_radius=0.01,point_width=2,side_width=1,point_color=colors.WHITE,side_color=colors.WHITE,area_color=colors.WHITE):
        """Create a material form."""
        self.points=points
        self.point_mode=point_mode
        self.point_radius=point_radius
        self.point_width=point_width
        self.side_width=side_width
        self.fill=fill
        self.area_color=area_color
        self.point_color=point_color
        self.side_color=side_color

    def getPointFromMaterialPoint(self,material_point):
        """Change the type of an instance of MaterialPoint into a Point type using material_point."""
        position=material_point.getPosition()
        x,y=position
        return Point(x,y)

    def getPosition(self):
        """Return the position of the center of the material form."""
        return self.form.center

    def getPoints(self):
        """Return the material points of the material form."""
        return self.points


    def getMotion(self):
        """Return the motion of the object."""
        return Motion.sum([motion for motion in self.points.getMotion()])

    def getMaterialPoints(self):
        """Return the material points of the form."""
        return self.points

    def setMaterialPoints(self,points):
        """Set the material points of the form."""
        self.points=points


    def show(self,window):
        """Show the form on the window."""
        form=self.getForm()
        form.show(window)

    def update(self,t=1):
        """Update the form by updating all its points."""
        for point in self.points:
            point.update(t)

    def rotate(self,angle=math.pi,center=Point(0,0)):
        """Rotate the form by rotating its points."""
        for point in self.points:
            point.rotate(angle,center)


    def getMass(self):
        """Calculate the mass of the form using its area and the mass of the material_points that define it."""
        """The way used to calculate it is arbitrary and should be improved."""
        form=self.getForm()
        mass=sum([point.mass for point in self.points])
        mass*=form.area()
        return mass

    def __getitem__(self,index):
        """Return the material point of number 'index'."""
        return self.points[index]

    def __setitem__(self,index,point):
        """Return the material point of number 'index'."""
        self.points[index]=point

    def getCenter(self):
        """Return the center of the material form."""
        center=MaterialPoint.createFromform.center
        x,y=center
        position=Vector(x,y,color=colors.GREEN)
        point_motion=Motion()
        for point in self.points:
            point_motion+=point.getMotion()
        material_center=MaterialPoint(point_motion)
        material_center.setPosition(position)
        return material_center

    def showMotion(self,surface):
        """Show the motion on a surface."""
        form=self.getForm()
        center=form.center()
        x,y=center
        position=Vector(x,y,color=colors.GREEN)
        point_motion=Motion()
        for point in self.points:
            point_motion+=point.getMotion()
        material_center=MaterialPoint(point_motion)
        material_center.setPosition(position)
        material_center.showMotion(surface)

    def getCollisionInstant(self,other):
        """Return the instant of the collision the material form with the other object."""
        pass

    def __or__(self,other):
        """Determine the points of intersections of the material point and another material object."""
        if isinstance(other,MaterialForm): return self.crossMaterialForm(other)

    def crossMaterialForm(self,other):
        """Return the material point of intersection between two material forms."""
        f1=self.getForm()
        f2=other.getForm()
        points=f1.crossForm(f2)
        points=[MaterialPoint.createFromPoint(point) for point in points]
        return points

    def getTrajectory(self,t=1):
        """Return the segments that are defined by the trajectory of each point."""
        segments=[Segment(p.getPosition(),p.getNextPosition) for p in self.points]
        return segments

    def affectFriction(self,frixion=None):
        """Reduce th velocity of the object according to its frixion."""
        f=self.factor
        for entity in self.entities:
            entity.velocity=[f*entity.velocity[0],f*entity.velocity[1]]



if __name__=="__main__":
    from .surface import Surface
    surface=Surface()
    c1=[-10,-10,10,10]
    f1=Form.random(c1)
    f1=MaterialForm.createFromForm(f1,[Force(0.001,0),Force(0,0.001)])

    c2=[-10,-10,10,10]
    f2=Form.random(c2)
    f2=MaterialForm.createFromForm(f2,[Force(0.001,0),Force(0,0.001)])

    #print(form[0].forces)
    #print(form.getMass())
    origin=Point(0,0)
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        f1.update(t=0.1)
        f2.update(t=0.1)
        f1.rotate(0.01,f1.center().getPoint())
        f2.rotate(-0.01,f2.center().getPoint())
        for p in f1|f2:
            p.show(surface,color=colors.RED)
        surface.draw.window.print("form.motion:"+str(f1.getPosition()),(10,10))
        f1.show(surface)
        f2.show(surface)
        f1.showMotion(surface)
        f2.showMotion(surface)
        surface.flip()
