from myabstract import Circle, Vector, Point
from mymotion import Motion
from mymaterial import Material
from myforce import Force
from mymanager import Manager

from pygame.locals import K_f
# from playsound import playsound # Doesn't work on macos

import mycolors
import random
import math

G = 6.67408e-11  # gravity constant of international system of units
ud = 1  # unit distance for computing
um = 1  # unit mass for computing
udd = 10e-10  # unit distance for visualizing
# if udd didn't exist the points would be too far away for pygame to handle


class Galaxy:
    def __init__(self):
        pass


class System:
    """System of astres."""

    @classmethod
    def distance(cls, astre1, astre2):
        """"Return the distance between 2 astes."""
        return math.sqrt(sum([(c1 - c2)**2 for (c1, c2) in zip(astre1.position, astre2.position)]))

    @classmethod
    def attraction(cls, astre1, astre2):
        """Return the force of attraction of the astre2 on the astre1."""
        norm = G * astre1.mass * astre2.mass / cls.distance(astre1, astre2)**2
        angle = (astre2.position - astre1.position).angle
        return Force.createFromPolarCoordonnates(norm, angle) / astre1.mass

    def random(n=10):
        """Create a random system."""
        astres = [Astre(name="Sun", radius=200)] + \
            [Astre.random() for i in range(n)]
        return System(astres)

    def __init__(self, astres):
        """Create the astes."""
        self.astres = astres

    def show(self, context):
        """Show all the astres."""
        self.showAstres(context)

    def showAstres(self, context):
        """Show all the astres."""
        for astre in self.astres:
            astre.show(context)

    def update(self, dt):
        """Update the astres."""
        self.updateAstresMotions()
        self.updateAstres(dt)

    def updateAstres(self, dt):
        """Update the asters individually."""
        for astre in self.astres:
            astre.update(dt)

    def updateAstresMotions(self):
        """Update the motions of the astres."""
        for i in range(len(self.astres)):
            self.updateAstreMotion(i)

    def updateAstreMotion(self, n):
        """Update the motion of the n-th astre."""
        f = Force.null()
        for i in range(len(self.astres)):
            if i != n:
                f += System.attraction(self.astres[n], self.astres[i])
        self.astres[n].acceleration = Vector(*f)


class Astre(Material):

    @classmethod
    def random(cls, na=5, sparse=1e10):
        """Create a random astre."""
        c = "bcdfghjklmnpqrstvwxyz"
        v = "aeiou"
        def rd(n): return c[random.randint(0, len(c) - 1)
                            ] if n % 2 == 0 else v[random.randint(0, len(v) - 1)]
        name = "".join([rd(i) for i in range(na)])
        radius = random.uniform(0, 1)
        mass = random.uniform(1e20, 1e26)
        position = 1e12 * Vector.random()
        velocity = 1e6 * Vector.random()
        velocity.angle = (position.angle + math.pi / 2) % (2 * math.pi)
        acceleration = Vector.null()
        motion = Motion(position, velocity, acceleration)
        color = mycolors.random()
        return cls(name, radius, mass, motion, color)

    def __init__(self, name="Unnamed", radius=1, mass=1, motion=Motion(), color=mycolors.WHITE):
        """"Create an astre using its name, radius, mass, motion and colors."""
        self.name = name
        self.mass = mass
        self.radius = radius
        self.motion = motion
        self.color = color

    def __str__(self):
        """Return the string representation of an astre."""
        return self.name + ":" + str(self.motion) + "," + str(self.mass)

    def show(self, context):
        """Show the astre."""
        self.showCircle(context)
        self.showMotion(context)
        self.showName(context)

    def showCircle(self, context):
        """Show the circle."""
        c = self.getCircle()
        c.show(context)

    def showMotion(self, context):
        """Show the motion of the astre."""
        (udd * self.velocity).show(context, udd * self.position)
        (udd * self.acceleration).show(context, udd * self.position)

    def showName(self, context):
        """Show the name of the astre."""
        c = Point(*(udd * self.position))
        c.showText(context, self.name, size=10, color=self.color)

    def update(self, dt):
        """Update the astre."""
        self.motion.update(dt)

    def getCircle(self):
        """Return the circle associated with the astre."""
        x, y = self.position
        r = self.radius
        x *= udd
        y *= udd
        r *= udd
        return Circle(x, y, radius=r, color=self.color)

    circle = property(getCircle)


class Planet(Astre):
    def __str__(self):
        """Return the string representation of a planet."""
        return "Planet:" + super().__str__()

    def computeMotion(self):
        """Find the motion of a planet with its distance and its mass."""
        angle = random.uniform(0, 2 * math.pi)
        norm = self.distance
        position = Vector.createFromPolarCoordonnates(norm, angle)
        angle = (angle + math.pi / 2) % (2 * math.pi)
        norm = self.speed  # in m/s-1
        velocity = Vector.createFromPolarCoordonnates(norm, angle)
        acceleration = Vector.null()
        return Motion(position, velocity, acceleration)


class Star(Astre):
    def __str__(self):
        """Return the string representation of a star."""
        return "Star:" + super().__str__()


class Sun(Star):
    def __init__(self):
        """Create the Sun with its physical data."""
        self.name = "Sun"
        self.mass = 1.989 * 1e30 * um
        self.radius = 695510 * 1e3 * ud
        self.motion = Motion()
        self.color = mycolors.YELLOW


class Mercury(Planet):
    def __init__(self):
        """Create Mercury with its physical data."""
        self.name = "Mercury"
        self.mass = 3.285 * 1e23 * um
        self.radius = 2439.7 * 1e3 * ud
        self.distance = 57.91 * 1e9 * ud
        self.speed = 175936 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.GREY


class Venus(Planet):
    def __init__(self):
        """Create Venus with its physical data."""
        self.name = "Venus"
        self.mass = 4.867 * 1e24 * um
        self.radius = 3389.5 * 1e3 * ud
        self.distance = 108.2 * 1e9 * ud
        self.speed = 126062 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.mix(mycolors.YELLOW, mycolors.LIGHTGREY)


class Earth(Planet):
    def __init__(self):
        """Create the Earth with its physical data."""
        self.name = "Earth"
        self.mass = 5.972 * 1e24 * um
        self.radius = 6051.8 * 1e3 * ud
        self.distance = 149.6 * 1e9 * ud
        self.speed = 107243 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.GREEN


class Mars(Planet):
    def __init__(self):
        """Create Mars with its physical data."""
        self.name = "Mars"
        self.mass = 6.39 * 1e23 * um
        self.radius = 6371 * 1e3 * ud
        self.distance = 227.9 * 1e9 * ud
        self.speed = 87226 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.RED


class Jupiter(Planet):
    def __init__(self):
        """Create Jupiter with its physical data."""
        self.name = "Jupiter"
        self.mass = 1.898 * 1e27 * um
        self.radius = 24622 * 1e3 * ud
        self.distance = 778.5 * 1e9 * ud
        self.speed = 47196 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.ORANGE


class Saturn(Planet):
    def __init__(self):
        """Create Saturn with its physical data."""
        self.name = "Saturn"
        self.mass = 5.683 * 1e26 * um
        self.radius = 25362 * 1e3 * ud
        self.distance = 1.434 * 1e12 * ud
        self.speed = 34962 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.mix(mycolors.YELLOW, mycolors.BROWN)


class Uranus(Planet):
    def __init__(self):
        """Create Uranus with its physical data."""
        self.name = "Uranus"
        self.mass = 8.681 * 1e25 * um
        self.radius = 69911 * 1e3 * ud
        self.distance = 2.871 * 1e12 * ud
        self.speed = 24459 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.lighten(mycolors.BLUE, 1)


class Neptune(Planet):
    def __init__(self):
        """Create Neptune with its physical data."""
        self.name = "Neptune"
        self.mass = 1.024 * 1e26 * um
        self.radius = 58232 * 1e3 * ud
        self.distance = 4.495 * 1e12 * ud
        self.speed = 19566 * 1e3 / 3600 * ud
        self.motion = self.computeMotion()
        self.color = mycolors.BLUE


class SystemManager(Manager):
    """Manage a space system. Note that all the values are in si units."""

    @classmethod
    def createSolarSystem(cls, **kwargs):
        """Create the solar system."""
        astres = [Sun(), Mercury(), Venus(), Earth(), Mars(),
                  Jupiter(), Saturn(), Uranus(), Neptune()]
        system = System(astres)
        return cls(system, **kwargs)

    @classmethod
    def createRandomSystem(cls, n=50, **kwargs):
        """Create a random system."""
        system = System.random(n=n)
        return cls(system, **kwargs)

    def __init__(self, system, **kwargs):
        """Create a system manager."""
        super().__init__(**kwargs)
        self.system = system
        self.dt = 3600  # 1 hour in seconds
        self.generateStars()

    def setup(self):
        """Play the sound."""
        # playsound('spacemusic.mp3')
        #raise NotImplementedError("The music doesn't work on pygame for macos.")

    def generateStars(self,):
        """Generate a picture of the stars."""
        self.stars = self.context.draw.window.loadImage("étoiles.jpg")
        self.stars = self.context.scale(self.stars, self.context.size)

    def update(self):
        """Update the system."""
        self.system.update(self.dt)

    def showLoop(self):  # Overloaded the function to delete the grid
        """Show the graphical components and deal with the context in the loop."""
        self.context.control()
        self.context.clear()
        self.show()
        self.showCamera()
        self.context.console.show()
        self.context.flip()

    def show(self):
        """Show the system."""
        self.showStars()
        self.system.show(self.context)
        if self.counter % 24 == 0:
            self.context.console("day:", self.counter // 24)

    def showStars(self):
        """Show random distant stars for the cool effect it gives."""
        self.context.draw.window.blit(self.stars, (0, 0))

    def reactKeyDown(self, key):
        """React to a key down event."""
        super().reactKeyDown(key)
        if key == K_f:  # Resize the background image when in fullscreen
            self.generateStars()


if __name__ == "__main__":
    sm = SystemManager.createSolarSystem()
    sm()
