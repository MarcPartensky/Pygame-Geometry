from .rectangle import Rectangle
from . import colors

import numpy as np


class Sprite(Rectangle):
    def __init__(self, position, size, grid, **kwargs):
        super().__init__(position, size, **kwargs)
        self.grid = grid

    def show(self, window):
        px, py = self.position
        sx, sy = self.size
        for y, line in enumerate(self.grid):
            for x, case in enumerate(line):
                window.draw.rect(window.screen, case, (x+px, y+py, sx, sy), 1)

    def save(self):
        """Save the sprite."""
        pass




