from mymanager import Manager
from mycontext import Context
from pygame.locals import *

import numpy as np
import mycolors

import os


class Mandelbrot(Manager):
    def compute(self, z):
        c = z
        for n in range(self.maxiter):
            if abs(z) > 2:
                return n
            z = z**2 + c
        return self.maxiter

    def __init__(self, name="Mandelbrot", precisions=[10, 5, 2, 1], maxiter=80, n=0):
        """Create a set of mandelbrot using the size, the corners and the maxiter (maxiteration)."""
        super().__init__(name)
        self.maxiter = maxiter
        self.precisions = precisions
        self.n = n

    def loop(self):
        """Code executed during the loop."""
        self.eventsLoop()
        self.checkUpdate()  # This technique allows to make calculations only when needed

    def setup(self):
        """Build the set before the loop."""
        self.updateLoop()
        self.showLoop()

    def update(self):
        """Build the matrix."""
        xmin, ymin, xmax, ymax = self.corners
        sx, sy = self.size
        dx = xmax - xmin
        dy = ymax - ymin
        self.matrix = np.zeros(self.size)
        for ix in range(sx):
            for iy in range(sy):
                x = xmin + dx * ix / sx
                y = ymin + dy * iy / sy
                z = complex(x, y)
                self.matrix[ix][iy] = self.compute(z)


    def show(self):
        """Show the mandelbrot set on the context."""
        xmin, ymin, xmax, ymax = self.corners
        sx, sy = self.size
        dx, dy = xmax - xmin, ymax - ymin
        csx, csy = self.context.size
        qsx, qsy = csx / sx, csy / sy
        cmax = np.max(self.matrix)
        cmin = np.min(self.matrix)
        dc = cmax - cmin
        for ix in range(self.width):
            for iy in range(self.height):
                c = int(255 * (self.matrix[ix][iy] - cmin) / dc)
                color = (c,c,c) #color = mycolors.colorRange((self.matrix[ix][iy] - cmin) / dc)
                x, y = csx * ix / sx, csy - csy * iy / sy
                self.context.draw.window.draw.rect(
                    self.context.screen, color, [x, y, qsx, qsy])

    def reactKeyDown(self, key):
        """React to an keydown event."""
        super().reactKeyDown(key)
        n = self.n
        if key == K_SPACE:
            self.n = (self.n + 1) % len(self.precisions)
        if key == K_1:
            self.n = 0
        if key == K_2:
            self.n = 1
        if key == K_3:
            self.n = 2
        if key == K_4:
            self.n = 3
        if key == K_f:
            self.refresh()
        if self.n != n:
            self.context.console("Precision set to: ", self.n + 1)
            self.refresh()

    def checkUpdate(self):
        """Detect is there is any update and refresh the screen if there is."""
        keys = self.context.press()
        if keys[K_DOWN] or keys[K_UP] or keys[K_LEFT] or keys[K_RIGHT] or keys[K_RSHIFT] or keys[K_LSHIFT]:
            if self.n != 0:
                self.context.console("Precision set to: ", 1)
            self.n = 0
            self.refresh()

    def refresh(self):
        """Refresh the set by updating the matrix and updating the screen."""
        self.updateLoop()
        self.showLoop()

    def getCorners(self):
        return self.context.corners

    def getWidth(self):
        return self.context.width // self.precisions[self.n]

    def getHeight(self):
        return self.context.height // self.precisions[self.n]

    def getSize(self):
        return [c // self.precisions[self.n] for c in self.context.size]

    # Properties
    corners = property(getCorners)
    height = property(getHeight)
    width = property(getWidth)
    size = property(getSize)


class MandelbrotVideo(Mandelbrot):
    """Create a video of the mandelbrot set while zooming."""

    def __init__(self, filename='mandelbrot.mp4',
                 name="Mandelbrot",
                 precision=1,
                 maxiter=80,
                 steps=50,
                 start_position=(0,0),
                 end_position=(0,0),
                 start_units=[200, 200],
                 end_units=[1000, 1000],
                 ** kwargs):
        """Create a mandelbrot object which goal is to make a video."""
        super().__init__(name, [precision], maxiter, **kwargs)
        self.context.switch()
        self.start_position = start_position
        self.end_position = end_position
        self.start_units = start_units
        self.end_units = end_units
        self.context.draw.plane.position = start_position
        self.context.draw.plane.units = start_units
        self.steps = steps
        self.context.camera.buildScreenWriter(filename)
        self.computeDUnits()

    def computeDUnits(self):
        """Compute the d units using its start_units, end_units and steps."""
        sux,suy=self.start_units
        eux,euy=self.end_units
        dux=(eux/sux)**(1/self.steps)
        duy=(euy/suy)**(1/self.steps)
        self.dunits=(dux,duy)
        print(self.dunits)

    def loop(self):
        self.eventsLoop()
        self.updateLoop()
        self.showLoop()

    def updateLoop(self):
        """Update the mandelbrot video by changing the position and the zoom."""
        self.updateZoom()
        self.update()
        self.context.camera.write()
        # self.context.console(self.context.counter,self.context.camera._draw.plane.units)
        self.checkEnd()
        self.context.count()

    def checkEnd(self):
        """Make sure that the recording is not over."""
        if self.context.counter > self.steps:
            self.context.camera.release()
            self.context.open = False

    def updateZoom(self):
        """Zoom inside the mandelbrot set."""
        ux, uy = self.context.draw.plane.units
        dux, duy = self.dunits
        ux *= dux
        uy *= duy
        self.context.draw.plane.units = [ux, uy]


dope_video_plan = {
    'filename':         'mandelbrot.mp4',
    'name':             'Mandelbrot',
    'precision':        1,
    'maxiter':          80,
    'steps':            1000,
    'start_position':   [-0.761574, -0.0847596],
    'end_position':     [-0.761574, -0.0847596],
    'start_units':      [200, 200],
    'end_units':        [1e13,1e13],
}


if __name__ == "__main__":
    # precisions = [10, 5, 2, 1]
    # maxiter = 80
    # corners = [-2, -1, 1, 1]
    # name = "Mandelbrot"
    # m = Mandelbrot(name, precisions, maxiter)
    # m.context.corners = corners
    # m()

    m = MandelbrotVideo(**dope_video_plan)
    m()
