from .motion import Motion
from .material import Material


class Physics(Material): #,Rotational?
    """Create a physical object that can have multiples motions for describing
    the way the objects move in any space. Because a physical object is also a
    material object it makes it easy to use in practice."""

    #Should a physical object possess a mass????????

    @classmethod
    def createFromNumber(cls,n,nm=3,d=2):
        """Create n motions."""
        return cls([Motion.null(n=nm,d=d) for i in range(n)])

    @classmethod
    def random(cls,n=2,nm=2,d=2):
        """Create n random physical objects."""
        return cls([Motion.random(n=nm,d=d) for i in range(n)])

    def __init__(self, motions=None, mass=1):
        """Create a physical object using its motions, by default a physical
        has 2 motions but it can have more.
        By default a physical object has a motion and a moment that are both
        nulls and 2 dimensionals."""
        if motions is None:
            motions = [Motion.null(n=3, d=2), Motion.null(n=2, d=1)]
        self.motions = motions
        self.mass = mass

    def __neg__(self):
        """Set to negative all the motions."""
        return Physics([-m for m in self.motions])

    def __add__(self, other):
        """Add two physical objects."""
        return Physics([m1 + m2 for (m1, m2) in zip(self.motions, other.motions)])

    def __sub__(self, other):
        """Substract 2 motions."""
        return self + (-other)

    def __str__(self):
        """Return the string representation of the physical object."""
        return "Physics(" + ",".join(map(str, self.motions)) + ")"

    # Properties
    def getMotion(self):
        """Return self.motions[0]."""
        return self.motions[0]

    def setMotion(self, motion):
        """Set self.motions[0]."""
        self.motions[0] = motion

    def getMoment(self):
        """Return self.motions[1]."""
        return self.motions[1]

    def setMoment(self, moment):
        """Set the moment."""
        self.motions[1] = moment

    def update(self, dt=1):
        """Update the physical object."""
        for motion in self.motions:
            motion.update(dt)

    def getPosition(self):
        """Return the position of the physical object."""
        return self.motion.position

    def setPosition(self, position):
        """Set the position of the physical object."""
        self.motion.position = position

    def getAngle(self):
        """Return the angle of the physical object."""
        return self.moment.position

    def setAngle(self, angle):
        """Set the angle of the physical object."""
        self.moment.position = angle

    motion = property(getMotion, setMotion)
    moment = property(getMoment, setMoment)
    position = property(getPosition, setPosition)
    angle = property(getAngle, setAngle)

    def getMomentum(self):
        """Return the momentum of the object, computed using the velocity and the mass."""
        return self.velocity * self.mass

    def setMomentum(self, momentum):
        """Set the momentum of the object, by changing its velocity."""
        self.velocity = momentum / self.mass

    momentum = property(getMomentum, setMomentum)

if __name__ == "__main__":
    #from .context import Context
    p1 = Physics.random()
    p2 = Physics.random()
    p3 = p1 - p2
    p3.update()
    print(p3)
