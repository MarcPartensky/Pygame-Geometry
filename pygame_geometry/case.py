from .abstract import Form, Point
from .pixel import Pixel
from .rectangle import Rectangle
from . import colors

from pygame.locals import *

import time


class TrueCase(Form):
    def __init__(self, *position, size=[1, 1], color=colors.WHITE, fill=True):
        """Create a case using the position and optional size, color and fill."""
        if len(position) == 1: position = position[0]
        self.position = list(position)
        self.size = size
        self.color = color
        self.fill = fill

    def getPoints(self):
        """Return the points of the case."""
        xmin, ymin, xmax, ymax = self.getCorners()
        p1 = Point(xmin, ymin)
        p2 = Point(xmax, ymin)
        p3 = Point(xmax, ymax)
        p4 = Point(xmin, ymax)
        return [p1, p2, p3, p4]

    def setPoints(self, points):
        """Set the points of the case by changing the position and the size.
        Because all the sets of points cannot match a pure rectangle, some
        approximations will be made. Technically only two points are necessary
        to create a rectangle."""
        xmin = min([p.x for p in pointss])
        xmax = max([p.x for p in points])
        ymin = min([p.y for p in points])
        ymax = max([p.y for p in points])
        corners = [xmin, ymin, xmax, ymax]
        coordonnates = self.getCoordonnatesFromCorners(corners)
        self.position = coordonnates[:2]
        self.size = coordonnates[2:]

    def __eq__(self, other):
        """Determine if two cases are the same by comparing its x and y components."""
        return self.position == other.position and self.size == other.size

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the position through an iteration."""
        if self.iterator < 2:
            value = self.position[self.iterator]
            self.iterator += 1
            return value
        else:
            raise StopIteration

    def getCenter(self):
        """Return the center of the case."""
        xmin, ymin, xmax, ymax = self.getCorners()
        x = (xmin + xmax) / 2
        y = (ymin + ymax) / 2
        return Point(x, y)

    def setCenter(self, point):
        """Set the center of the case."""
        sx, sy = self.size
        px, py = self.point
        self.position = [px + sx / 2, py + sy / 2]

    def show(self, surface, **kwargs):
        """Show the case. By default it only show the associated form."""
        self.showForm(surface, **kwargs)

    def showText(self, surface, text):
        """Show the text on the surface."""
        point = self.center()
        point.showText(surface, text)

    def showForm(self, surface, fill=None, area_color=None, side_color=None):
        """Show the pixel on screen."""
        f = self.getForm(fill, area_color, side_color)
        f.show(surface)

    def __str__(self):
        """Return the string representation of the object."""
        return "case(" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def getCorners(self):
        """Return the corners of the case."""
        px, py = self.position
        sx, sy = self.size
        return (px, py, px + sx, py + sy)

    def setCorners(self):
        """Set the corners of the case."""
        coordonnates = self.getCoordonnatesFromCorners(corners)
        self.position = coordonnates[:2]
        self.size = coordonnates[2:]

    def __contains__(self, position):
        """Determine if the point is in the paint."""
        x, y = position
        xmin, ymin, xmax, ymax = self.getCorners()
        return (xmin <= x <= xmax) and (ymin <= y <= ymax)

    center = property(getCenter, setCenter, "Allow the user to manipulate the center of the case easily.")
    points = property(getPoints, setPoints, "allow the user to manipulate the points of the case easily")


class Case(Pixel):
    def __init__(self, *position, size=[1, 1], color=colors.WHITE, fill=True):
        """Create a pixel."""
        if len(position) == 1:
            position = position[0]
        self.position = position
        self.size = size
        self.color = color
        self.fill = fill

    def __eq__(self, other):
        """Determine if two cases are the same by comparing its x and y components."""
        return self.position == other.position

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < 2:
            value = self.position[self.iterator]
            self.iterator += 1
            return value
        else:
            raise StopIteration

    def getForm(self, fill=None, area_color=None, side_color=None):
        """Return the abstract form associated with the case."""
        if not fill: fill = self.fill
        if not area_color: area_color = self.color
        if not side_color: side_color = colors.WHITE
        xmin, ymin, xmax, ymax = self.getCorners()
        p1 = Point(xmin, ymin)
        p2 = Point(xmax, ymin)
        p3 = Point(xmax, ymax)
        p4 = Point(xmin, ymax)
        points = [p1, p2, p3, p4]
        return Form(points, fill=fill, side_color=side_color, area_color=area_color, point_show=False)

    def getCenter(self):
        """Return the center of the case."""
        xmin, ymin, xmax, ymax = self.getCorners()
        x = (xmin + xmax) / 2
        y = (ymin + ymax) / 2
        return Point(x, y)

    def setCenter(self, point):
        """Set the center of the case."""
        sx, sy = self.size
        px, py = self.point
        self.position = [px + sx / 2, py + sy / 2]

    def show(self, surface, **kwargs):
        """Show the case. By default it only show the associated form."""
        self.showForm(surface, **kwargs)

    def showText(self, surface, text):
        """Show the text on the surface."""
        point = self.center()
        point.showText(surface, text)

    def showForm(self, surface, fill=None, area_color=None, side_color=None):
        """Show the pixel on screen."""
        f = self.getForm(fill=fill, area_color=area_color, side_color=side_color)
        f.show(surface)

    __getitem__ = lambda self, i: self.position[i]

    # def __getitem__(self,index):

    def __str__(self):
        """Return the string representation of the object."""
        return "case(" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def getCorners(self):
        """Return the corners of the case."""
        px, py = self.position
        sx, sy = self.size
        return (px, py, px + sx, py + sy)

    def __contains__(self, position):
        """Determine if the point is in the paint."""
        x, y = position
        xmin, ymin, xmax, ymax = self.getCorners()
        return (xmin <= x <= xmax) and (ymin <= y <= ymax)

    center = property(getCenter, setCenter, "Allow the user to manipulate the center of the case easily.")


if __name__ == "__main__":
    from .context import Surface
    from .zone import Zone

    # surface=Surface(plane=Zone(size=[20,20]))
    surface = Surface()
    cases = [Case([x, y], color=colors.random(), fill=True) for x in range(-20, 20) for y in range(0, 20)]
    cases = [Case([x, y], color=colors.GREEN, fill=True) for x in range(8) for y in range(8)]
    # cases=[]
    matrix = [[None for i in range(8)] for y in range(8)]
    for x in range(8):
        for y in range(8):
            matrix[x][y] = Case([x, y], color=colors.GREEN, fill=True)
            # case=Case([x,y],color=colors.GREEN,fill=True)
            # if x%8==0 or y%8==0:
            #    case.color=colors.BLUE
            # cases.append(case)
    # matrix[1][1].color=colors.BLUE
    # matrix[1][0].color=colors.BLUE

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        for case in cases:
            case.show(surface)
        surface.flip()
