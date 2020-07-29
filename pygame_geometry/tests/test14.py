from myabstract import Form, Point
from mymanager import Manager

import mycolors


class Tester(Manager):
    def __init__(self, *args, **kwargs):
        self.form = Form.random(n=10)
        self.focus = 0
        super().__init__(*args, **kwargs)

    def update(self):
        self.form.points[self.focus].set(self.context.point())

    def reactMouseButtonDown(self, button, position):
        if button == 1:
            position = self.context.getFromScreen(position)
            p = Point.closest(Point(*position), self.form.points)
            self.focus = self.form.points.index(p)

    def show(self):
        self.form.show(self.context)
        c = self.form.getBornCircleSlow()
        # f.color = mycolors.RED
        # f.show(self.context)
        for i, point in enumerate(self.form.points):
            point.showText(self.context, str(point), size=2)
        c.center.show(self.context, color=mycolors.GREEN, mode="cross")
        c.show(self.context, color=mycolors.GREEN)

    def show2(self):
        f.color = mycolors.YELLOW
        c2 = f.getCirclePassingByThreePoints()
        f.show(self.context)
        c1.center.show(self.context, color=mycolors.GREEN, mode="cross")
        c1.show(self.context, color=mycolors.GREEN)
        c2.center.show(self.context, color=mycolors.BLUE, mode="cross")
        c2.show(self.context, color=mycolors.BLUE)

if __name__ == "__main__":
    t = Tester()
    t()