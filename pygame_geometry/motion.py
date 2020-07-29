from .abstract import Vector, Point
from . import colors

import copy
import math


class Motion:
    # Class methods
    # Operations
    @classmethod
    def null(cls, n=3, d=2):
        """Return the neutral motion."""
        # The dimension d still needs to be implemented for the vectors.
        return cls([Vector.null(d=d) for i in range(n)])

    neutral = zero = null

    @classmethod
    def sum(cls, motions):
        """Return the sum of the motions together."""
        result = cls.null()
        for motion in motions:
            result += motion
        return result

    @classmethod
    def average(motions):
        """Return the average of the motions."""
        return cls.sum(motions) / len(motions)

    # Random
    @classmethod
    def random(cls, n=3, d=2, borns=[-1, 1], **kwargs):
        """Create a random motion using optional minimum and maximum."""
        vectors = [Vector.random(d=d, borns=borns, **kwargs) for i in range(n)]
        return cls(*vectors)

    # Object functions
    # Initializing

    def __init__(self, *vectors):
        """Create a motion using vectors."""
        if len(vectors) > 0:
            if isinstance(vectors[0], list):
                vectors = vectors[0]
        self.vectors = list(vectors)
        if len(self.vectors) >= 1:
            self.position.color = colors.GREEN
        if len(self.vectors) >= 2:
            self.velocity.color = colors.BLUE
        if len(self.vectors) >= 3:
            self.acceleration.color = colors.RED

    # Set
    def set(self, other, n=None):
        """Set the components of the motion to the components of another motion
        without affecting its colors."""
        if n is None: n = len(self.vectors)
        for i in range(n):
            self.vectors[i].set(other.vectors[i])

    def showEach(self, context):
        """Show the motion on the screen from the origin of the plane."""
        for vector in self.vectors:
            vector.show(context)

    # Showing
    def show(self, context):
        """Show the vectors from the position."""
        for vector in self.vectors[1:]:
            vector.show(context, self.position)

    # Updating the motion
    def update(self, dt=1):
        """Update the motion according to physics."""
        l = len(self.vectors)
        for i in range(1, l):
            self.vectors[-i - 1] += self.vectors[-i] * dt

    # Representation
    def __str__(self):
        """Return the str representation of the motion."""
        return "mt(" + ",".join(map(str, self.vectors)) + ")"

    # Iterations
    def __iter__(self):
        """Iterate the vectors."""
        self.iterator = 0
        return self

    def __next__(self):
        """Return the next vector of the iteration."""
        if self.iterator < len(self.vectors):
            self.iterator += 1
            return self.vectors[self.iterator - 1]
        else:
            raise StopIteration

    # Time behaviour
    def next(self, t=1):
        """Return the next motion using its actual one using optional time t."""
        acceleration = Vector([a for a in self.acceleration])
        velocity = Vector([v + a * t for (v, a) in zip(self.velocity, self.acceleration)])
        position = Vector([p + v * t for (p, v) in zip(self.position, self.velocity)])
        return Motion(position, velocity, acceleration)

    def previous(self, t=1):
        """Return the previous motion using its actual one using optional time t."""
        acceleration = Vector([a for a in self.acceleration])
        velocity = Vector([v - a * t for (v, a) in zip(self.velocity, self.acceleration)])
        position = Vector([p - v * t for (p, v) in zip(self.position, self.velocity)])
        return Motion(position, velocity, acceleration)

    # Length
    def __len__(self):
        """Return the number of vectors."""
        return len(self.vectors)

    # Items
    def __getitem__(self, index):
        """Return the vector of index 'index.'"""
        return self.vectors[index]

    def __setitem__(self, index, vector):
        """Set the vector of index 'index.'"""
        self.vectors[index] = vector

    # Vectors
    # Position
    def getPosition(self):
        """Return the position of the motion."""
        return self.vectors[0]

    def setPosition(self, position):
        """Set the position of the motion using position."""
        self.vectors[0] = position

    def delPosition(self):
        """Set the position to zero."""
        self.vectors[0] = Vector([0 for i in range(len(self.vectors[0].position))])

    # Velocity
    def getVelocity(self):
        """Return the velocity of the motion."""
        return self.vectors[1]

    def setVelocity(self, velocity):
        """Set the velocity of the motion using velocity."""
        self.vectors[1] = velocity

    def delVelocity(self):
        """Set the velocity to zero."""
        self.vectors[1] = Vector([0 for i in range(len(self.vectors[1].position))])

    # Acceleration
    def getAcceleration(self):
        """Return the acceleration of the motion."""
        return self.vectors[2]

    def setAcceleration(self, acceleration):
        """Set the acceleration of the motion."""
        self.vectors[2] = acceleration

    def delAcceleration(self):
        """Set the acceleration to zero."""
        self.vectors[2] = Vector([0 for i in range(len(self.vectors[2].position))])

    # Operations

    def __neg__(self):
        """Return the motions made of the negative vectors."""
        return Motion(*[-v for v in self.vectors])

    __radd__ = __add__ = lambda self, other: Motion(*[v1 + v2 for (v1, v2) in zip(self.vectors, other.vectors)])  # Addition
    __rsub__ = __sub__ = lambda self, other: Motion(*[v1 - v2 for (v1, v2) in zip(self.vectors, other.vectors)])  # Substraction
    __rmul__ = __mul__ = lambda self, other: Motion(*[v * other for v in self.vectors])  # Multiplication
    __rtruediv__ = __truediv__ = lambda self, other: Motion(*[v / other for v in self.vectors])  # Division
    __rfloordiv__ = __floordiv__ = lambda self, other: Motion(*[v // other for v in self.vectors])  # Floor Division

    def __iadd__(self, other):
        """Add the other motion to the motion."""
        self.set(self + other)
        return self

    def __isub__(self, other):
        """Substract the other motion to the motion."""
        self.set(self - other)
        return self

    def __imul__(self, other):
        """Multiply a motion by a scalar."""
        self.set(self * other)
        return self

    def __itruediv__(self, other):
        """Divide a motion by a scalar."""
        self.set(self / other)
        return self

    def __ifloordiv__(self, other):
        """Divide motion by a scalar according to euclidian division."""
        self.set(self // other)
        return self

    # Properties
    position = property(getPosition, setPosition, delPosition, "Allow the user to manipulate the position.")
    velocity = property(getVelocity, setVelocity, delVelocity, "Allow the user to manipulate the velocity.")
    acceleration = property(getAcceleration, setAcceleration, delAcceleration,
                            "Allow the user to manipulate the acceleration.")
    # Other derivatives in order...
    # jerk=property(getJerk,setJerk,delJerk,"Representation of the jerk.")
    # snap=jounce=property(getSnap,setSnap,delSnap,"Representation of the snap.")
    # crackle=property(getCrackle,setCrackle,delCrackle,"Representation of the crackle.")
    # pop=property(getPop,setPop,delPop,"Representation of the pop.")


class Moment(Motion):
    """A moment is a motion that correspond to the angular momentum of an object.
    The only difference here are the default parameters such as the dimensions,
    the number of vectors and the colors."""

    # Instance methods
    # Initializing
    def __init__(self, *vectors, n=2, d=1):
        """Create a motion using vectors."""
        if len(vectors) > 0:
            if isinstance(vectors[0], list):
                vectors = vectors[0]
        self.vectors = list(vectors)
        if len(self.vectors) >= 1:
            self.position.color = colors.PURPLE
        if len(self.vectors) >= 2:
            self.velocity.color = colors.ORANGE
        if len(self.vectors) >= 3:
            self.acceleration.color = colors.YELLOW

    # Representation
    def __str__(self):
        """Return the str representation of the moment."""
        return "mm(" + ",".join(map(str, self.vectors)) + ")"

    # Showing
    def show(self, context, point=Point(0, 0), angle=0):
        """Show the moment."""
        if len(self) >= 1:
            mp = self.position
            v = Vector.createFromPolar(mp.norm, angle)
            v.color = mp.color
            v.show(context, point)
        if len(self) >= 2:
            angle += math.pi / 2
            mv = self.velocity
            v = Vector.createFromPolar(mv.norm, angle)
            v.color = mv.color
            v.show(context, point)
        if len(self) >= 3:
            angle += math.pi / 2
            ma = self.acceleration
            a = Vector.createFromPolar(ma.norm, angle)
            a.color = ma.color
            a.show(context, point)


if __name__ == "__main__":
    from .context import Context

    context = Context(name="Motion Demonstration")
    motion1 = Motion.random()
    motion2 = Motion.random()
    motion = motion1 + motion2
    motion = Motion.sum([Motion.random() for i in range(9)] + [motion])  # Summing 10 motions together
    moment = Moment.random()
    print(motion, moment)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        motion.show(context)
        moment.show(context)
        context.flip()
