from .rectangle import Rectangle
from .window import Window
from .zone import Zone
from .rect import Rect
from . import colors

import numpy as np
import random
import noise
import os


class Component:
    def __init__(self, color=(0, 255, 0)):
        """Create a component."""
        self.color = color

    def show(self, window, position, size):
        """Show the component on the screen's using window, position and size."""
        window.draw.rect(window.screen, self.color,
                         position + [size[0] + 1, size[1] + 1], 0)

    def save(self, directory):
        """Save the component for later use."""


class Grass(Component):
    def __init__(self):
        self.grid = [[0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]

    def show(self, window, position, size):
        pass


# class DeprecatedMap(Zone):
#     def __init__(self, size=[20, 20], theme={}, view=None):
#         """Create a map using size, theme, view, components"""
#         Zone.__init__(self, size=size, theme=theme, view=view)
#         self.size = size
#         sx, sy = self.size
#
#     def edit(self, window):
#         pass
#         self.grid = [[Component() for x in range(sx)] for y in range(sy)]
#
#     def fill(self, position, value):  # This method is totally useless
#         """Fill the position with the given value."""
#         x, y = position
#         self.grid[y][x] = value
#
#     def showPlane(self, window):
#         """Show the map on the window."""
#         self.showGrid(window)
#         self.showCases(window)
#         self.showBorders(window)
#
#     def showCases(self, window):
#         """Show all the components on screen."""
#         sx, sy = self.size
#         nx = sx // 2
#         ny = sy // 2
#         for y in range(sy):
#             for x in range(sx):
#                 position = self.getToScreen([x - nx, y - ny + 1], window)
#                 self.grid[y][x].show(window, position, self.units)


class Map(Rectangle):
    """A simple map is basically just a map with a grid of values, and each
    value correspond to a type of case."""
    @classmethod
    def random(cls, size=(10, 10), ncases=10):
        """Create a random simple map."""
        cases = [colors.random() for i in range(ncases)]
        w, h = size
        grid = [[random.randint(0, 9) for x in range(w)] for y in range(h)]
        grid = np.array(grid)
        return cls(grid, cases)

    def __init__(self, grid, cases):
        """Create a simple map that is centered in the origin."""
        self.grid = grid
        self.cases = cases
        w, h = list(reversed(self.grid.shape[:2]))
        super().__init__((w//2, h//2), (w, h))

    def show(self, context):
        """Show the simple map on the context."""
        w, h = self.size
        for y in range(h):
            for x in range(w):
                color = self.cases[int(self.grid[y][x])]
                context.draw.rect(context.screen, color, (x, y+1) + (1, 1), 1)
        super().show(context)


if __name__ == "__main__":
    from .manager import Manager

    class Tester(Manager):
        def __init__(self):
            """Create a tester for the simple map using no arguments."""
            super().__init__()
            self.map = Map.random()

        def show(self):
            self.map.show(self.context)

    t = Tester()
    t()
