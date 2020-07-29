from mymanager import Manager
from myabstract import Form, Point
from pygame.locals import *

import mycolors
import random
import noise
import math


class PerlinAsteroid:
    def __init__(self, position=[0, 0], color=mycolors.WHITE, precision=100, radius=0.01, conversion=True):
        """Create a perlin asteroid using its optional position and initial_phase."""
        self.position = position
        self.color = color
        self.precision = precision
        self.conversion = conversion
        self.radius = radius
        self.noise_max = 2
        self.phase = random.uniform(0, 100)
        self.phase_dt = 0.01
        self.wo = 2 * math.pi
        self.form = self.getForm()

    def __str__(self):
        """Str representation of a perlin noise asteroid."""
        return "PerlinAsteroid(position:" + str(self.position) + ")"

    def update(self):
        """Update the perlin asteroid."""
        self.form = self.getForm()
        self.phase += self.phase_dt

    def show(self, context):
        """Show the form."""
        self.form.show(context)

    def getPoints(self):
        """Return the points of the perlin asteroid."""
        points = []
        wo = self.wo
        nm = self.noise_max
        off = self.phase
        px, py = self.position
        for i in range(self.precision):
            a = i / self.precision * wo
            xoff = nm * (math.cos(a + off) + 1) / 2
            yoff = nm * (math.sin(a + off) + 1) / 2
            r = noise.pnoise2(xoff + off, yoff + off)
            r = (r + 1) / 2
            x = r * math.cos(a)
            y = r * math.sin(a)
            points.append((px + x, py + y))
        return points

    def getForm(self):
        """Return the form of the perlin asteroid."""
        #points=[Point(*p) for p in self.getPoints()]
        return Form.createFromTuples(self.getPoints(), conversion=self.conversion, radius=self.radius, side_color=self.color)

    def log(self, context):
        """Allow an easy debug of the asteroid."""
        text = [
            "Asteroid:log:",
            "precision:" + str(self.precision),
            "phase:" + str(self.phase),
            "color:" + str(self.color),
            "phase_dt:" + str(self.phase_dt),
            "wo:" + str(self.wo)
        ]
        context.console.appendLines(text)


class PerlinNoiseLoop(Manager):
    def __init__(self, name="PerlinNoiseLoop Demonstration"):
        """Initialize the perlin noise loop manager."""
        super().__init__(name=name)
        self.circle_precision = 100
        self.circle_color = mycolors.WHITE
        self.noise_max = 2
        self.phase = 0
        self.phase_dt = 0.01
        self.wo = 2 * math.pi

    def update(self):
        self.circle = self.getCircle()
        self.phase += self.phase_dt

    def reactKeyDown(self, key):
        super().reactKeyDown(key)
        if key == K_DOWN:
            self.noise_max -= 0.1
        if key == K_UP:
            self.noise_max += 0.1

    def show(self):
        self.showCircle()
        # self.showPerlinNoise()

    def showCircle(self):
        self.context.draw.lines(self.context.screen,
                                self.circle_color, self.circle, connected=True)

    def getCircle(self):
        """Return the list of points that correspond to the circle of the perlin noise loop."""
        circle = []
        wo = self.wo
        nm = self.noise_max
        off = self.phase
        for i in range(self.circle_precision):
            a = i / self.circle_precision * wo
            xoff = nm * (math.cos(a + off) + 1) / 2
            yoff = nm * (math.sin(a + off) + 1) / 2
            r = noise.pnoise2(xoff + off, yoff + off)
            r = (r + 1) / 2
            x = r * math.cos(a)
            y = r * math.sin(a)
            circle.append((x, y))
        return circle

    def showPerlinNoise(self, precision=100):
        """Show the perlin noise in 2d space on the context."""
        s = 1 / precision
        for ix in range(precision):
            for iy in range(precision):
                x = ix / precision
                y = iy / precision
                c = noise.pnoise2(x * 50, y * 50)
                c = int(255 * (c + 1) / 2)
                self.context.draw.rect(
                    self.context.screen, (c, c, c), (x, y, s, s), fill=True)


class PerlinAsteroidManager(Manager):
    def __init__(self, n=10):
        super().__init__()
        def rp(): return [random.uniform(-10, 10), random.uniform(-10, 10)]
        self.asteroids = [PerlinAsteroid(rp()) for i in range(n)]

    def show(self):
        self.showAsteroids()

    def showAsteroids(self):
        for asteroid in self.asteroids:
            asteroid.show(self.context)

    def update(self):
        self.updateAsteroids()

    def updateAsteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()


if __name__ == "__main__":
    pam = PerlinAsteroidManager()
    pam()
