from .abstract import Point, Segment, Form, Circle, Vector, Line
from .curves import Trajectory

import random


# Interface Anatomy
# - show(context)   //an anatomy must be responsible for drawing itself
# - __str__()           //an anatomy must be able to give a string representation
# - __contains__(point) //an anatomy must be able to tell if a point is in it
# - cross(anatomy)  //an anatomy must be able to determine if it is crossing another anatomy
# - collide(anatomy)
# - recenter()
# - update()
# . center          //an anatomy must have a center

# image, segment and form implement anatomy


class Anatomy:
    """Interface anatomy."""
    def __str__(self):
        """Add an 'a' for 'anatomy'."""
        return "a"+super().__str__()

    # def enlarge(self, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    # @classmethod
    # def random(cls, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def __init__(self, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def update(self, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def show(self, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def rotate(self, *args, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def cross(self, other, **kwargs):
    #     raise NotImplementedError("This method must be overloaded.")
    #
    # def collide(self, other):
    #     raise NotImplementedError("This method must be overloaded.")


class PointsAnatomy(Anatomy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updateBorn()

    def updateBorn(self):
        """Return the born of the anatomy."""
        c = self.center
        lengths = [Point.distance(c, p) for p in self.points]
        self._born = max(lengths)

    def getBorn(self):
        return self._born

    def setBorn(self, born):
        self._born = born

    born = property(getBorn)

    def enlarge(self, n):
        center = self.center
        for point in self.points:
            v = n * Vector.createFromTwoPoints(center, point)
            point.set(v(point))
        # self._born *= n
        self.updateBorn()


class CircleAnatomy(Circle, Anatomy):
    def updateBorn(self):
        pass

    def rotate(self, *args, **kwargs):
        pass

    def getBorn(self):
        return self.radius

    def setBorn(self, born):
        self.radius = born

    born = property(getBorn, setBorn)

    def collide(self, other):
        """Determine if 2 circle anatomies are colliding."""
        v1 = Vector(*self.center)
        v2 = Vector(*other.center)
        return (v1-v2).norm < self.radius + other.radius


class TrajectoryAnatomy(PointsAnatomy, Trajectory):
    @classmethod
    def random(cls, nmin=5, nmax=20):
        """Create a random trajectory anatomy."""
        n = random.randint(nmin, nmax)
        ru = random.uniform
        points = [(ru(-10, 10), ru(-10, 10)) for i in range(n)]
        return cls.createFromTuples(points)

    def rotate(self, angle):
        """Rotate around its center."""
        c = Point(*self.center)
        for point in self.points:
            point.rotate(angle, c)

    def getCenter(self):
        return Point.average(self.points)

    def setCenter(self, center):
        shift = center - self.center
        for point in self.points:
            point += shift

    center = property(getCenter, setCenter)

    def collide(self, other):
        """Determine if 2 trajectories are colliding."""
        for s1 in self.segments:
            for s2 in other.segments:
                if s1.cross(s2):
                    return True
        return False


class FormAnatomy(PointsAnatomy, Form):
    def collide(self, other):
        """Determine if the forms are colliding."""
        for p in self.points:
            if p in other:
                return True
        for p in other.points:
            if p in self:
                return True
        return False


class SegmentAnatomy(PointsAnatomy, Segment):
    def collide(self, other):
        return self.p1 in other or self.p2 in other


class LineAnatomy(Line):
    def collide(self, other):
        """Determine if 2 lines are colliding."""
        return not self.parallel(other)

    def getCenter(self):
        return self.point

    def setCenter(self, center):
        self.point = center

    center = property(getCenter, setCenter)

    def getBorn(self):
        return float('inf')

    def setBorn(self):
        pass

    born = property(getBorn, setBorn)


if __name__ == "__main__":
    from .manager import BodyManager
    from .body import Body

    ta = TrajectoryAnatomy.random()
    ca = CircleAnatomy.random()
    fa = FormAnatomy.random()
    sa = SegmentAnatomy.random()
    la = LineAnatomy.random()

    tb = Body.createFromRandomMotions(ta)
    cb = Body.createFromRandomMotions(ca)
    fb = Body.createFromRandomMotions(fa)
    sb = Body.createFromRandomMotions(sa)
    lb = Body.createFromRandomMotions(la)

    print(sa.born)

    m = BodyManager(tb, cb, fb, sb, lb)
    m()
