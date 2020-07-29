from myabstract import Line, Segment, Point, Form, HalfLine

from copy import deepcopy

import numpy as np
import math

import mycolors


class Ray(HalfLine):
    """The ray spreads like a line but must stop when an object is hit."""

    def __init__(self, *args, **kwargs):
        """Create a light ray."""
        super().__init__(*args, **kwargs)

    def show(self, surface, point):
        """Show the ray on the surface and stop at the given point."""
        if point:
            object = Segment(self.point, point)
        else:
            object = HalfLine(self.point, self.angle)
        object.show(surface)

    def __str__(self):
        """Return the string representation of a ray."""
        return "ray(" + str(self.point) + "," + str(self.angle) + ")"


class Emiter:
    """The emiter send light."""

    def __init__(self, position=[0, 0], n=50, view=[0, 2 * math.pi]):
        """Create an emiter object."""
        x, y = position
        self.point = Point(x, y)
        self.n = n
        self.view = view

    def show(self, surface, points):
        """Show the emiter and with its rays on the given surface."""
        for i in range(self.n):
            self.rays[i].show(surface, points[i])

    def update(self, surface):
        """Update the emiter using the surface."""
        p = surface.point()
        if p:
            self.point = Point(p)
            vx, vy = self.view
            self.rays = [Ray(self.point, a) for a in np.linspace(vx, vy, self.n)]


class RayCaster:
    def __init__(self, emiter=Emiter([0, 0]), forms=[]):
        """Create a ray casting object idea from the coding train on youtube."""
        self.emiter = emiter
        self.forms = forms  # Forms tp be displayed by the caster

    def __call__(self, surface):
        """Main loop of the caster."""
        while surface.open:
            surface.check()
            surface.control()
            surface.clear()
            surface.show()
            self.update(surface)
            self.show(surface)
            surface.flip()

    def addForm(self, form):
        """Add a form to the ray caster."""
        self.forms.append(form)

    def removeForm(self, form):
        """Remove a form to the ray caster."""
        self.forms.remove(form)

    def hasForm(self, form):
        """Determine if the ray caster has a form."""
        return form in self.forms

    def show(self, surface):
        """Show the ray caster on the given surface along with its rays and the forms."""
        for form in self.forms:
            form.show(surface)
        points = self.getPoints()
        self.emiter.show(surface, points)

    def getPoints(self):
        """Return the list of points for each ray if there are crossing with one of the forms of the ray caster."""
        points = []
        for ray in self.emiter.rays:
            rp = ray.point
            p = None
            for form in self.forms:
                cross = form.crossHalfLine(ray)
                if cross:
                    np = cross[0]
                    if p:
                        p1 = p - rp
                        p2 = np - rp
                        if p2 < p1:
                            p = np
                    else:
                        p = np
            points.append(p)
        return points

    def update(self, surface):
        """Update the ray caster."""
        self.emiter.update(surface)


if __name__ == "__main__":
    from mycontext import Surface
    from myzone import Zone

    surface = Surface(name="RayCasting", plane=Zone())
    # forms=[Form.random([-10,-10,10,10],number=5,side_color=mycolors.RED) for i in range(10)]
    forms = [Form.random([10 * (i - 5), -5, 10 * (i - 4), 5], number=5, side_color=mycolors.RED) for i in range(10)]
    # forms=[Segment.random([10*(i-5),-5,10*(i-4),5],number=5,side_color=mycolors.RED) for i in range(10)]
    emiter = Emiter()
    caster = RayCaster(emiter, forms)
    origin = Point(0, 0)

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        for form in forms:
            form.rotate(0.1, origin)
        caster.update(surface)
        caster.show(surface)
        surface.flip()
