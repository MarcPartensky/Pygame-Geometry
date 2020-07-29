from .abstract import Form,Point,Segment,Vector,Circle
from . import colors

class Angle(float):
    def createFromThreePoints(points):
        """Create an angle from 3 points."""
        p1,p2,p3=points
        v1=Vector.createFromTwoPoints(p2,p1)
        v2=Vector.createFromTwoPoints(p2,p3)
        angle=v2.angle()-v1.angle()
        return Angle(angle)

    def __new__(self,value):
        """Create a new angle."""
        return float.__new__(self,value)

    def __init__(self,value):
        """Create an angle object."""
        float.__init__(value)

    def __str__(self):
        """Return the string representation of the angle."""
        return str(float(self))+" C"

    def show(self,surface,points):
        """Show the angle between the points."""
        p1,p2=points
        #Need to be able to print arc of circles using pygame
        v1=Vector.createFromTwoPoints(p1,p2)
        v1=~v1
        v2=v1%self
        p3=v2(p2)
        s1=Segment(p1,p2)
        s2=Segment(p2,p3)
        s1.show(surface)
        s2.show(surface)
        #I need to show arc of circles which im too lazy to do now




if __name__=="__main__":
    from .surface import Surface
    surface=Surface()
    corners=[-10,-10,10,10]
    f=Form.random(corners,number=5,side_width=3,side_color=mycolors.RED)
    p=f.points
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        f.show(surface)
        f.rotate(0.001)
        l=len(f)
        for i in range(l):
            h=(i+l-1)%l
            j=(i+1)%l
            angle=Angle.createFromThreePoints([p[h],p[i],p[j]])
            angle.show(surface,[p[h],p[i]])
            c=Circle.createFromPointAndRadius(p[i],1,fill=Falses)
            c.show(surface,color=mycolors.GREEN)
        surface.flip()
    a=Angle(3)
    print(a)
