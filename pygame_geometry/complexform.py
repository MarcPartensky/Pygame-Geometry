from .abstract import Form,Point,Segment
from . import colors

import numpy as np
import random

class ComplexForm(Form):
    """The fact that complex from inherits from Form involves overloading all
    specific methods of forms which make sense in a complex form but cannot work.
    This choice was made out of pure lazyness."""

    def __init__(self,*args,**kwargs):
        """Create a complex form."""
        super().__init__(*args,**kwargs)
        l=len(self.points)
        self.network=np.zeros((l,l))
        self.network.fill(1)
        self.network=np.triu(self.network)
        self.network[0][0]=0
        self.network[0][3]=0
        self.network[3][3]=0

    def getSegments(self):
        """Return the segments determined by the points and the network established."""
        segments=[]
        l=len(self.points)
        for j in range(l):
            for i in range(j):
                if self.network[i][j]:
                    segment=Segment(self.points[i],self.points[j])
                    segments.append(segment)
        return segments

    def setSegments(self,segments):
        """Set the segments of the complex form."""
        self.points=list(set([s.p1 for s in segments]+[s.p2 for s in segments]))
        l=len(self.points)
        self.network=np.zeros((l,l))
        for s in segments:
            i=self.points.index(s.p1)
            j=self.points.index(s.p2)
            if i>j: i,j=j,i
            self.network[i][j]=1

    def delSegments(self):
        """Delete the segments of the complex form."""
        self.points=[]
        self.network=np.array([])

    def show(self,surface):
        """Show the complex form on the surface."""
        self.showPoints(surface)
        self.showSegments(surface)
        self.showCrossPoints(surface)

    def getRegions(self):
        """Decompose the complex forms in multiple normal forms which cannot be cut by a segment."""
        vectors=[Vector.createFromSegment(segment) for segment in self.segments()]
        for j in range(l):
            for i in range(j):
                if self.network[i][j]:
                    segment=Segment(self.points[i],self.points[j])
                    vector=x
                    segments.append(segment)

        for vector in vectors:
            pass

        return segments

    def crossSelf(self,e=10e-10):
        """Return the list of the points of intersections between the form and itself."""
        results=[]
        for i in range(len(self.segments)):
            for j in range(i):
                point=self.segments[i].crossSegment(self.segments[j])
                if point: results.append(point)
        return results


    def split(self):
        """Return all the system of forms that compose the complex forms."""
        links=[(p,0) for p in self.points]

    def countContacts(self):
        """Return the list of contacts for each points, which means how many points
        is a given point connected to."""
        return [np.sum(self.network[:][j]) for j in range(len(self.points))]

    segments=property(getSegments,setSegments,delSegments,"Allow the user to manipulate the segments of the form.")


if __name__=="__main__":
    from .context import Surface
    from .plane import Plane
    p = Plane(theme={"grid nscale": 2})
    surface = Surface(name="Complex Form", plane=p)
    arguments = {
        "n": 5,
        "cross_point_color": colors.GREEN,
        "cross_point_mode": 1,
        "cross_point_size": (0.01, 0.01),
        "cross_point_width": 2
    }
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        for p in f:
            p.rotate(0.01)
        f.show(surface)
        surface.flip()
