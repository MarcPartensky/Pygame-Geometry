from mybody import SimpleBody
from mymanager import BodyManager
from myperlinnoiseloop import PerlinAsteroid
from mymotion import Motion

from copy import deepcopy
import mycolors


class BodyManagerModified(BodyManager):
    def update(self):
        """Update the bodies."""
        self.updateBodies()
        self.follow(self.context.point())

    def follow(self, p):
        """Follow the cursor."""
        for body in self.bodies:
            body.follow(p)


class Asteroid(PerlinAsteroid):
    """This class is the result of the adapter pattern."""
    def getCenter(self):
        return self.position

    center = property(getCenter)


class AsteroidBody(SimpleBody):
    @classmethod
    def random(cls, nm=1, nv=2, d=2):
        """Create a random asteroid."""
        anatomy = Asteroid(color=mycolors.random(),conversion=False,radius=5)
        motions = [Motion.random(n=nv, d=d) for im in range(nm)]
        return cls(anatomy, motions)

    def update(self, dt):
        """Update the asteroid body."""
        self.anatomy.update()
        self.motion.update(dt)

    def getAbsolute(self):
        """Return the absolute anatomy of the body which means its form after
        changing the position depending on its motion."""
        anatomy = deepcopy(self.anatomy)
        anatomy.position=self.motion.position  # change its position
        anatomy.update()
        return anatomy



bmm=BodyManagerModified.createRandomBodies(AsteroidBody,dt=0.1) #This class is just made to test bodies quickly
bmm()
