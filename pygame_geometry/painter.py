from .case import Case
from .abstract import Point, Form
from . import colors

import numpy as np
import shelve

from pygame.locals import *


class Painter:
    def __init__(self, *args, **kwargs):
        """Create a painter."""
        self.paints = [Board(), Paint(*args, **kwargs)]
        self.paint_brush = PaintBrush()
        self.painting = 0

    def __call__(self, surface):
        """Main loop of the painter."""
        while surface.open:
            surface.check()
            surface.control()
            surface.clear()
            surface.show()
            self.show(surface)
            self.control(surface)
            surface.flip()

    def control(self, surface):
        """Control the painter."""
        cursor = surface.point()
        cursor = [round(c + 1 / 2) for c in cursor]
        self.print(surface)
        self.paint(surface)

    def print(self, surface):
        """Print the state of the painter on the surface."""
        if self.painting == None:
            surface.print("Create a new painting.", [-10, 12])

    def paint(self, surface):
        """Paint using the surface and the paint."""
        keys = surface.press()
        click = surface.click()
        cursor = surface.point()
        cursor = [round(c + 1 / 2) for c in cursor]

        self.paint_brush.setPosition(cursor)

        p = self.getPaint(cursor)
        if p is not None:
            c = self.paints[p].getCase(cursor)

        if keys[K_r]:
            self.paint_brush.setRandomColor()
        if keys[K_a]:
            self.paint_brush.lightenColor()
        if keys[K_b]:
            self.paint_brush.darkenColor()
        if keys[K_f]:
            self.refreshBoard()
        if p is None:
            if click:
                self.createPaint(cursor)
            return

        if keys[K_s]:
            self.save(self.paints[p])
        if keys[K_l]:
            self.load(p)

        if c is None:
            return

        if keys[K_c]:
            self.paint_brush.copyColor(self.paints[p].cases[c])

        if not click:
            return
        self.paint_brush.paint(surface, self.paints[p], c)

    def createPaint(self, position):
        """Create a paint."""
        size = [20, 20]
        self.paints.append(Paint(position, size))

    def save(self, paint):
        """Save the paint."""
        print("File saved")
        with shelve.open('paints') as p:
            p["test"] = paint

    def load(self, p):
        """Load a paint."""
        print("File loaded")
        with shelve.open("paints") as paints:
            paint = paints["test"]
        self.paints[p] = paint

    def refreshBoard(self):
        """Change the colors of the board."""
        self.paints[0].generate()

    def show(self, surface):
        """Show the paints of the painter."""
        for paint in self.paints:
            paint.show(surface)
        self.paint_brush.show(surface)

    def getPaint(self, position):
        """Return the case containing the position if there is one."""
        for i in range(len(self.paints)):
            if position in self.paints[i]:
                return i


class PaintBrush:
    def __init__(self, position=[0, 0], size=[1, 1], color=colors.GREEN):
        """Create a paint brush for the painter."""
        self.position = position
        self.size = size
        self.color = color

    def paint(self, surface, paint, c):
        """Color a case."""
        paint.cases[c].color = self.color

    def copyColor(self, case):
        """Copy the color of the case."""
        self.color = case.color

    def setRandomColor(self):
        """Set the color of the brush to a random color."""
        self.color = colors.random()

    def lightenColor(self, surface):
        """Lighten the brush."""
        self.color = colors.lighten(self.color)

    def darkencolor(self, surface):
        """Darken the color."""
        self.color = colors.darken(self.color)

    def setPosition(self, position):
        """Set the position of the brush."""
        self.position = position

    def show(self, surface):
        """Show the paint brush on the surface."""
        x, y = self.position
        case = Case((x - 1, y - 1), size=self.size, color=self.color)
        case.show(surface, fill=False, side_color=colors.RED)


class Paint:
    """Paint object reserves an area to draw objects in."""

    @classmethod
    def random(cls, position=[0, 0], size=[10, 10]):
        """Create a random paint."""
        return cls(position, size)

    def __init__(self, position=[0, 0], size=[10, 10]):
        """Create a board object."""
        self.position = position
        self.size = size
        self.cases = []
        self.generate()

    def getCorners(self):
        """Return the corners of the paint."""
        px, py = self.position
        sx, sy = self.size
        corners = (px, py, px + sx, py + sy)
        return corners

    def generate(self):
        """Generate random cases all over the paint."""
        cases = []
        xmin, ymin, xmax, ymax = self.getCorners()
        for y in np.arange(ymin, ymax):
            for x in np.arange(xmin, xmax):
                case = Case([float(x), float(y)], color=colors.WHITE)
                cases.append(case)
        self.cases = cases

    def __contains__(self, position):
        """Determine if the point is in the paint."""
        x, y = position
        xmin, ymin, xmax, ymax = self.getCorners()
        return (xmin <= x <= xmax) and (ymin <= ymax)

    def getCase(self, position):
        """Return the case containing the position if there is one."""
        for i in range(len(self.cases)):
            if position in self.cases[i]:
                return i

    def getForm(self):
        """Return the form corresponding to the area of the painting."""
        xmin, ymin, xmax, ymax = self.getCorners()
        ps = [Point(xmin, ymin), Point(xmax, ymin),
              Point(xmax, ymax), Point(xmin, ymax)]
        return Form(ps)

    def show(self, surface):
        """Show the paint by showing all its cases."""
        f = self.getForm()
        for case in self.cases:
            case.show(surface, side_color=colors.WHITE)
        f.side_color = colors.WHITE
        f.side_width = 3
        f.show(surface)

    def save(self):
        """Save the paint."""
        with shelve.open('paints') as paints:
            paints[test] = self


class Board(Paint):
    def __init__(self):
        """Create an accesory for the painter."""
        self.position = [-12, -10]
        self.size = [1, 20]
        self.generate()

    def generate(self):
        """Generate random cases for the board."""
        x, y = self.position
        sx, sy = self.size
        self.cases = [Case([x, y - sy // 2], color=colors.random())
                      for y in range(sy)]

    def show(self, surface):
        """Show the paint by showing all its cases."""
        f = self.getForm()
        for case in self.cases:
            case.show(surface, side_color=colors.BLACK)
        f.side_color = colors.BLACK
        f.side_width = 3
        f.show(surface)
        f[0].showText(surface, "Board")


if __name__ == "__main__":
    from .context import Surface
    from .zone import Zone
    surface = Surface(name="Painter")
    painter = Painter([0, 0], [8, 8])
    #print([0,0] in painter.paints[0])
    painter(surface)
