"""This program is deprecated."""

from .abstract import Point, Form
from .materialform import MaterialForm

import random


class Brick(MaterialForm):
    @classmethod
    def random(cls, borns=[-1, 1], **kwargs):
        """Create a random brick."""
        position = [random.randint(*borns) for i in range(2)]
        return cls(position, **kwargs)

    def __init__(self, position, **kwargs):
        """Create a brick using its position."""
        points = self.getCornersPointsFromPosition(position)
        form = Form(points)
        form.makeSparse()
        form = MaterialForm.createFromForm(form)
        # material_points=[MaterialPoint.createFromPoint(point) for point in points]
        material_points = form.getMaterialPoints()
        super().__init__(material_points, **kwargs)

    def getCornersFromPosition(self, position):
        """Return the corners of the brick using a position."""
        x, y = position
        mx = x
        my = y
        Mx = x + 1
        My = y + 1
        return (mx, my, Mx, My)

    def getCornersPointsFromPosition(self, position):
        """Return the points which correspond to the corners of the brick."""
        corners = self.getCornersFromPosition(position)
        mx, my, Mx, My = corners
        points = [Point(x, y) for x in [mx, Mx] for y in [my, My]]
        return points


if __name__ == "__main__":
    from .context import Context
    surface = Context()
    # brick=Brick([0,0])
    bricks = [Brick.random(-10, 10) for i in range(10)]
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        for brick in bricks:
            brick.rotate(0.1)
            brick.show(surface)
        surface.flip()
