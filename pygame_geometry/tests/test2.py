from myabstract import Form, Point, HalfLine

from mycontext import Surface
import mycolors

surface = Surface(name="Test")

ps = [Point(-1, -1), Point(1, -1), Point(1, 1), Point(-1, 1)]
f = Form(ps)

while surface.open:
    surface.check()
    surface.control()
    surface.clear()
    surface.show()

    position = tuple(surface.point())
    p = Point(*position)
    h = HalfLine(p, 0)
    ps = f.crossHalfLine(h)

    print(ps)

    f.color = mycolors.WHITE
    if p in f:
        f.color = mycolors.RED
    if len(ps) % 2 == 1:
        f.color = mycolors.ORANGE

    h.show(surface)
    f.show(surface)
    surface.flip()
