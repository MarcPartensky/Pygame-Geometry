from .abstract import Form, Point
from . import colors

from pygame.locals import *

import copy

"""
class Box(Form):
    def __init__(self,*args,**kwargs):
        Create a box object.
        super().__init__(self,*args,**kwargs)

"""


class Box(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = None

    def showAll(self, surface):
        self.show(surface)
        self.showName(surface)

    def showName(self, surface):
        center = self.center()
        center.showText(surface, self.name)


class Diagram:
    def __init__(self):
        """Create a diagram object."""
        self.box = None
        self.boxes = []
        self.n = 0

    def __call__(self, surface):
        """Main loop."""
        while surface.open:
            surface.check()
            surface.control()
            surface.clear()
            surface.show()
            self.update(surface)
            self.show(surface)
            surface.flip()

    def show(self, surface):
        """Show the boxes on the surface."""
        self.point.show(surface)
        if self.box:
            self.box.show(surface)
        for boxe in self.boxes:
            boxe.showAll(surface)

    def getEvents(self, surface):
        """Save the necessary events."""
        self.point = Point(surface.point(), color=colors.RED)
        self.point.truncate()
        self.click = surface.click()
        self.keys = surface.press()

    def update(self, surface):
        """Update the diagram."""
        self.getEvents(surface)
        if self.keys[K_SPACE]:
            self.deleteBox()
        if self.click:
            if self.isInBox():
                i = self.selectBox()
                self.nameBox(i)
            else:
                if not self.box != None:
                    self.createBox()
                else:
                    if self.point != self.box.points[-1]:
                        if len(self.box) < 4:
                            self.addPointToBox()
                        else:
                            self.endBox()

    def isInBox(self):
        """Determine if a point is in a box."""
        for box in self.boxes:
            if self.point in box:
                return True
        return False

    def selectBox(self):
        """Select a box."""
        for i in range(len(self.boxes)):
            if self.point in self.boxes[i]:
                return i

    def createBox(self):
        """Create a box."""
        point = copy.deepcopy([self.point])
        self.box = Box(point)

    def addPointToBox(self):
        """Add a point to a box"""
        point = copy.deepcopy(self.point)
        self.box.addPoint(point)
        self.n += 1

    def endBox(self):
        """End the creation of the box."""
        box = copy.deepcopy(self.box)
        self.boxes.append(box)
        self.box = None

    def deleteBox(self):
        """Delete the actual box."""
        self.box = None

    def nameBox(self, i):
        """Select a box."""
        self.boxes[i].name = "Boite"


if __name__ == "__main__":
    from .surface import Surface

    surface = Surface()
    diagram = Diagram()
    diagram(surface)
