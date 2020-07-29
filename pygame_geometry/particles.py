from .manager import Manager
from .physics import Physics
from .abstract import Point, Vector
from .motion import Motion

import math


class Particle(Physics):
    """Representation of a particle."""
    made = 0
    @classmethod
    def random(cls, **kwargs):
        """Create a random particle using its motions' dimensions."""
        return cls([Motion.random(n=3, d=2), Motion.random(n=2, d=1)], **kwargs)

    def __init__(self, motions, name=None, mass=1):
        """Create a particle using its motions."""
        super().__init__(motions, mass=mass)
        Particle.made += 1
        if name is None:
            name = "prt" + str(Particle.made)
        self.name = name

    def showAll(self, context):
        """Show the particle and its name."""
        self.show(context)
        # self.showName(context)
        self.showComponents(context)

    def show(self, context):
        """Show a point."""
        self.point.show(context)
        self.vector.show(context, self.point)

    def showName(self, context):
        """Show the name of the particle."""
        self.point.showText(context, self.name, size=10, conversion=True)

    def showComponents(self, context):
        """Show the str of the particle."""
        self.point.showText(context, str(self), size=10, conversion=True)

    def getPoint(self):
        """Return the points associated with the particle."""
        return Point(*self.position)

    def getVector(self):
        """Return the vector associated with the rotation of the particle."""
        angle = self.angle[0]
        angle %= (2 * math.pi)
        return Vector.createFromPolar(1, angle)

    def getSpin(self):
        """The spin of a particle stays unclear for now..."""
        return self.angle[0]

    point = property(getPoint)
    vector = property(getVector)
    spin = property(getSpin)


class ParticleGroup:
    """Group of particles"""
    @classmethod
    def random(cls, n):
        """Create n random particles."""
        return cls([Particle.random() for i in range(n)])

    def __init__(self, particles):
        """Create the particle group using the list of all particles."""
        self.particles = particles

    def show(self, context):
        """Show all particles."""
        for particle in self.particles:
            particle.showAll(context)

    def __getitem__(self, index):
        """Return the particle of index 'index'."""
        return self.particles[index]

    def update(self, dt):
        """Update the particle group."""
        self.soloUpdate(dt)

    def soloUpdate(self, dt):
        """Update all the particles independently of the others."""
        for particle in self.particles:
            particle.update(dt)

    def updateFromSpin(self):
        """Technically, the particles with the same spin will repel themselves,
        whereas the particles with opposed spins will attract themselves."""
        # Good luck............
        raise NotImplementedError

    def attract(self):
        """Attract a particle to another."""
        # p=m1*v1=m2*v2
        # a=m1*v1**2=m2*v2**2

    def getDistance(self, p1, p2):
        """Return the distance between p1 and p2."""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def getDistances(self, p1, ps):
        """"Return the distances of the particles from p1."""
        return [self.getDistance(p1, ps) for p in ps]


class ParticlesManager(Manager):
    def __init__(self, n=10, dt=1e-2):
        """Create the particles manager."""
        super().__init__()
        self.particle_group = ParticleGroup.random(n)
        self.context.console(n, 'particles created')
        self.dt = dt

    def show(self):
        """show the particles."""
        self.particle_group.show(self.context)

    def update(self):
        """Update the particles."""
        self.particle_group.update(self.dt)

    def updateForces(self):
        """Update the forces of the particles."""

    def getParticles(self):
        """Return the particles group."""
        return self.particle_group

    def setParticles(self, particles):
        """Set the particle group."""
        self.particle_group = particles

    def getTime(self):
        """Return the time based on the counter and the dt."""
        return self.dt * self.counter

    def reactKeyDown(self, key):
        super().reactKeyDown(key)
        pass

    particles = property(getParticles, setParticles)
    t = time = property(getTime)


if __name__ == "__main__":
    m = ParticlesManager()
    m.context.console(m.particles[0])
    m()
