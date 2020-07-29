from .plane import Plane
from .window import Window
from .rect import Rect

from . import colors


class Zone(Plane, Rect):
    def __init__(self, size=[20, 20], theme={}, view=None):
        Plane.__init__(self, theme, view)
        self.size = size
        if not "borders_color" in theme:
            self.theme["borders_color"] = (255, 255, 255)

    def show(self, window):
        """Show the zone on the screen's window."""
        self.showGrid(window)
        self.showBorders(window)

    def showBorders(self, window):
        """Show the borders with a different color."""
        mx, my, Mx, My = self.getCorners(window)
        p = [(mx, my), (mx, My), (Mx, My), (Mx, my)]
        for i in range(len(p)):
            j = (i + 1) % len(p)
            start = p[i]
            end = p[j]
            start = self.getToScreen(start, window)
            end = self.getToScreen(end, window)
            window.draw.line(window.screen, self.theme["borders_color"], start, end, 1)

    def getCorners(self, window):
        """Return the corners of the present view."""
        sx, sy = self.size
        corners = (-sx // 2, -sy // 2, sx // 2, sy // 2)
        return corners


class ReversedZone(Zone):
    """Contrary to the zone when a wall is crossed the objects of the zone reappear to the other side of the zone."""

    def __init__(self, *args, **kwargs):
        """Create a reverse zone object."""
        super().__init__(*args, **kwargs)

    def getToScreen(self, position, window):
        """Return a screen position using a position in the plane."""
        x, y = position[0], position[1]
        px, py = self.position
        ux, uy = self.units
        wsx, wsy = window.size
        x = int((x - px) * ux + wsx / 2)
        y = int(wsy / 2 - (y - py) * uy)
        sx, sy = self.size
        xmin, ymin, xmax, ymax = self.getCorners(window)
        while x >= xmax:
            x -= sx
        while x < xmin:
            x += sx
        while y >= ymax:
            y -= sy
        while y < ymin:
            y += sy
        return [x, y]


if __name__ == "__main__":
    window = Window(fullscreen=True)
    zone = ReversedZone([10, 10])
    zone(window)
