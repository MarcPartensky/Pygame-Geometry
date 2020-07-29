from mymanager import BodyManager
from myabstract import Point, Segment, Form
import math
import random


class SierpinskiTriangle:
    @classmethod
    def new(cls, **kwargs):
        """Create a random SierpinskiTriangle."""
        triangle = []
        for i in range(3):
            a = i / 3 * 2 * math.pi
            x = math.cos(a)
            y = math.sin(a)
            triangle.append(Point(x, y))
        return cls(triangle, **kwargs)

    def __init__(self, triangle, points=[], n=0, nmax=5000, steps=10, radius=1e-5):
        """Create a sierpinski triangle."""
        self.triangle = triangle
        self.points = points
        self.point = Point.random()
        self.n = n
        self.steps = steps
        self.radius = radius

    def computePointBySteps(self):
        """Compute a new point."""
        for i in range(self.steps):
            r = random.randint(0, 2)
            s = Segment(self.point, self.triangle[r])
            self.point = s.middle
            self.point.radius = self.radius
            self.points.append(self.point)

    def computePoint(self):
        """Compute a new point."""
        r = random.randint(0, 2)
        s = Segment(self.point, self.triangle[r])
        self.point = s.middle
        self.point.radius = self.radius
        self.points.append(self.point)

    def computePoints(self):
        """Compute n points."""
        self.points = []
        p = Point.random()
        for i in range(self.nmax):
            r = random.randint(0, 2)
            s = Segment(p, self.triangle[r])
            p = s.middle
            self.points.append(p)

    def show(self, context):
        """Show the sierpinski triangle."""
        self.showTriangle(context)
        self.showPoints(context)
        self.showPointsNumber(context)

    def showPointsNumber(self, context):
        """Show the points number."""
        w = context.width
        context.draw.print("points number: " + str(len(self.points)), (w - 200, 20), conversion=False)

    def showTriangle(self, context):
        """Show the triangle."""
        Form(self.triangle).show(context)

    def showPoints(self, context):
        """Show all the points."""
        for point in self.points:
            point.show(context)

    def update(self, dt):
        """Compute a new point every update."""
        self.computePointBySteps()


if __name__ == "__main__":
    s = SierpinskiTriangle.new()
    bm = BodyManager(s, fullscreen=True)
    bm()
