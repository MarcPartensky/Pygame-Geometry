from .abstract import Segment
from .material import Material
from .materialpoint import MaterialPoint

class MaterialSegment(Material,Segment):
    """Material match of the abtract segment."""
    def null(d=2):
        """Return the neutral element of the material segment."""
        return MaterialSegment([MaterialPoint.null(d) for i in range(2)])

    def random(corners=[-1,-1,1,1]):
        """Return a random material segment within the given corners."""
        return MaterialSegment([MaterialPoint.random(corners) for i in range(2)])

    def __init__(self,*points,motion=None):
        """Create a material segment using the points p1 and p2."""
        if len(points)==1: points=points[0]
        if len(points)!=2: raise Exception("A segment can only have 2 points.")
        self.points=points
        Material.__init__(self.center,motion)


    def getCenter(self):
        """Return the material center of the segment."""
        return MaterialPoint.average(self.points)

    def setCenter(self,np):
        """Set the center of the material segment."""
        p=self.getCenter()
        v=Vector.createFromTwoPoints(np,p)
        self.points=[v(p) for p in self.points]


    def getP1(self):
        """Return the first point."""
        return self.points[0]

    def setP1(self,p1):
        """Set the first point."""
        self.points[0]=p1

    def getP2(self):
        """Return the second point."""
        return self.points[1]

    def setP2(self,p2):
        """Set the second point."""
        self.points[1]=p2

    p=center=property(getCenter,setCenter,"Representation of the material center of the segment.")
    p1=property(getP1,setP1,"Representation of the first material point of the material segment.")
    p2=property(getP2,setP2,"Representation of the second material point of the material segment.")

if __name__=="__main__":
    from .surface import Context
    context=Context()
    ms=MaterialSegment.random()
