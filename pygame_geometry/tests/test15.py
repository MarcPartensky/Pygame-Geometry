from myabstract import Line, Segment
from mymanager import AbstractManager
from myrectangle import Square

import mycolors
import random


class AbstractTester(AbstractManager):
    def __init__(self, *args, angle=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = angle
        self.square = Square.random(color=mycolors.PURPLE)

    def update(self):
        # random.shuffle(self.group)
        self.updateCollision()
        self.rotate()
        for l in self.group:
            if isinstance(l, Line):
                l.point.set(self.context.point())
                break

    def updateCollision(self):
        for e in self.group:
            e.color = mycolors.GREEN
        for i, e1 in enumerate(self.group):
            for e2 in self.group[1+i:]:
                print(e1, e2)
                p1 = e1.cross(e2)
                p2 = e2.cross(e1)
                if p1 or p2:
                    self.context.console(p1, p2)
                    e1.color = mycolors.RED
                    e2.color = mycolors.RED

    def rotate(self):
        for element in self.group:
            element.rotate(self.angle)

    def show(self):
        # self.group[0].showWithinCorners(self.context)
        self.square.show(self.context)
        corners = self.square.getCorners()
        #print(corners)
        for e in self.group:
            if isinstance(e, Line):
                e.showWithinCorners(self.context, [-1, -1, 2, 2])
            else:
                e.show(self.context)


if __name__ == "__main__":
    l1 = Line.random()
    l2 = Line.random()
    s = Segment.random()
    s1 = Segment.createFromTuples((-1, 0), (1, 0))
    s2 = Segment.createFromTuples((0, -1), (0, 1))
    m = AbstractTester(s, s1, s2, l1)
    m()
