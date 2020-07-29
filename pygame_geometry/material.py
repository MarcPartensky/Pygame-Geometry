import copy
from .abstract import Vector


class Material:
    """The material class is a class that contains a motion attributes and lots of
    properties that help its users to change its motion by using shorcuts.
    The user can consider a material object solely instead of modifying directly its
    motion which makes it an easy tool to use for 2d visualisations and games."""

    def __init__(self, motion):
        """Create a material object from its motion. This method doesn't necessarily
        need to be called since a motion property can replace it."""
        self.motion = motion

    # Class functions
    # Mathematical operations
    def sum(objects):
        """Return the sum of the objects."""
        result = copy.deepcopy(objects[0])
        result.motion = Motion.sum([object.motion for object in objects])
        return result

    def average(objects):
        """Return the average of the objects."""
        return Material.sum(objects) / len(objects)

    # Object functions
    # Vectors
    # Position
    def getPosition(self):
        """Return the position of the material point."""
        return self.motion.getPosition()

    def setPosition(self, position):
        """Set the position of the material point."""
        self.motion.position = Vector(position)

    def delPosition(self):
        """Set the position of the material point to (0,0)."""
        l = len(self.motion.position.components)
        for i in range(l):
            self.motion.position.components[i] = 0

    # Velocity
    def getVelocity(self):
        """Return the velocity of the material point."""
        return self.motion.getVelocity()

    def setVelocity(self, velocity):
        """Set the velocity of the material point."""
        self.motion.velocity = Vector(velocity)

    def delVelocity(self):
        """Set the position of the material point to (0,0)."""
        l = len(self.motion.velocity.components)
        for i in range(l):
            self.motion.velocity.components[i] = 0

    # Acceleration
    def getAcceleration(self):
        """Return the acceleration of the material point."""
        return self.motion.getAcceleration()

    def setAcceleration(self, acceleration):
        """Set the acceleration of the material point."""
        self.motion.acceleration = Vector(acceleration)

    def delAcceleration(self):
        """Set the position of the material point to (0,0)."""
        l = len(self.motion.acceleration.components)
        for i in range(l):
            self.motion.acceleration.components[i] = 0

    # Components
    # Position
    def getX(self):
        """Return the x component of the position of the point."""
        return self.motion.position.components[0]

    def getY(self):
        """Return the y component of the position of the point."""
        return self.motion.position.components[1]

    def setX(self, x):
        """Set the x component of the position of the point."""
        self.motion.position.components[0] = x

    def setY(self, y):
        """Set the y component of the position of the point."""
        self.motion.position.components[1] = y

    def delX(self):
        """Set the x component of the point to 0."""
        self.motion.position.components[0] = 0

    def delY(self):
        """Set the y component of the point to 0."""
        self.motion.position.components[1] = 0

    # Velocity
    def getVx(self):
        """Return the x component of the velocity of the point."""
        return self.motion.velocity.components[0]

    def getVy(self):
        """Return the y component of the velocity of the point."""
        return self.motion.velocity.components[1]

    def setVx(self, vx):
        """Set the vx component of the velocity of the point."""
        self.motion.velocity.components[0] = vx

    def setVy(self, vy):
        """Set the y component of the velocity of the point."""
        self.motion.velocity.components[1] = vy

    def delVx(self):
        """Set the x component of the velocity of the point to 0."""
        self.motion.velocity.components[0] = 0

    def delVy(self):
        """Set the y component of the velocity of the point to 0."""
        self.motion.position.components[1] = 0

    # Acceleration
    def getAx(self):
        """Return the x component of the acceleration of the point."""
        return self.motion.acceleration.components[0]

    def getAy(self):
        """Return the y component of the acceleration of the point."""
        return self.motion.acceleration.components[1]

    def setAx(self, vx):
        """Set the vx component of the acceleration of the point."""
        self.motion.acceleration.components[0] = vx

    def setAy(self, vy):
        """Set the y component of the acceleration of the point."""
        self.motion.acceleration.components[1] = vy

    def delAx(self):
        """Set the x component of the acceleration of the point to 0."""
        self.motion.acceleration.components[0] = 0

    def delAy(self):
        """Set the y component of the acceleration of the point to 0."""
        self.motion.position.components[1] = 0

    # Operations
    # Addition
    def __add__(self, other):
        """Return the addition of two material objects together."""
        object = copy.deepcopy(self)
        object.motion += other.motion
        return object

    def __iadd__(self, other):
        """Add a material object to another."""
        self.motion += other.motion
        return self

    __radd__ = __add__

    # Substraction
    def __sub__(self, other):
        """Return the subtraction of two material objects together."""
        object = copy.deepcopy(self)
        object.motion -= other.motion
        return object

    def __isub__(self, other):
        """Substract a material object to another."""
        self.motion -= other.motion
        return self

    __rsub__ = __sub__

    # Multiplication
    def __mul__(self, other):
        """Return the product of a material object with a scalar."""
        object = copy.deepcopy(self)
        object.motion *= other
        return object

    def __imul__(self, other):
        """Multiply the material object with a scalar."""
        self.motion *= other
        return self

    # Division
    # True division
    def __truediv__(self, other):
        """Return the division of the material object by a scalar."""
        object = copy.deepcopy(self)
        object.motion /= other
        return object

    def __itruediv__(self, other):
        """Divide the material object by a scalar."""
        self.motion /= other
        return self

    __rtruediv__ = __itruediv__

    # Floor division
    def __floordiv__(self, other):
        """Return the quotient in the Euclidian division of the material object by a scalar."""
        object = copy.deepcopy(self)
        object.motion //= other
        return object

    def __ifloordiv__(self, other):
        """Apply the quotient in the Euclidan division of the material object by a scalar."""
        self.motion //= other
        return self

    __rfloordiv__ = __ifloordiv__

    # Items
    def __getitem__(self, index):
        """Return the components of the position."""
        return self.motion.position[index]

    def __setitem__(self, index, value):
        """Set the components of the position."""
        self.motion.position[index] = value

    # Iterations
    # def __iter__(self):
    #    pass

    def rotate(self, angle, position):
        """Rotate the motion."""
        self.motion.rotate(angle, position)

    def rotatePosition(self, angle, position):
        """Rotate the position vector of the motion."""
        # self.motion.position.rotate(angle,position)

    position = property(getPosition, setPosition, delPosition, "Representation of the position of the material object.")
    velocity = property(getVelocity, setVelocity, delVelocity, "Representation of the velocity of the material object.")
    acceleration = property(getAcceleration, setAcceleration, delAcceleration,
                            "Representation of the acceleration of the material object.")
    x = property(getX, setX, delX, "Representation of the x component of the position of the material object.")
    y = property(getY, setY, delY, "Representation of the y component of the position of the material object.")
    vx = property(getVx, setVx, delVx, "Representation of the x component of the velocity of the material object.")
    vy = property(getVy, setVy, delVy, "Representation of the y component of the velocity of the material object.")
    ax = property(getAx, setAx, delAx, "Representation of the x component of the acceleration of the material object.")
    ay = property(getAy, setAy, delAy, "Representation of the y component of the acceleration of the material object.")
