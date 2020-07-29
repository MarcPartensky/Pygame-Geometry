from .abstract import Vector, Point
from .motion import Motion
from . import colors

p = 2  # Number of digits of precision of the objects when displayed


class Force(Vector):
    @classmethod
    def null(cls, d=2):
        """Return the null force."""
        return cls([0 for i in range(d)])

    neutral = zero = null

    @classmethod
    def sum(cls, forces, d=2):
        """Return the sum of the forces."""
        result = cls.null(d)
        for force in forces:
            result += force
        return result

    def __init__(self, *args, **kwargs):
        """Create a force."""
        super().__init__(*args, **kwargs)
        self.d = 0

    def __call__(self, physical_object):
        """Apply a force on the acceleration."""
        physical_object.acceleration.set(self.abstract.components)

    def show(self, context, position, m=8, n=2):
        """New dope show method especially for the forces."""
        v = self.abstract
        x, y = position
        nx, ny = v(position)
        v.show(context, position, color=self.color)
        w = v / m
        # color=colors.lighten(self.color)
        color = colors.WHITE
        for i in range(n):
            if (self.d + 2 * i) % m < (self.d + 1 + 2 * i) % m:
                w1 = (self.d + 2 * i) % m * w
                w2 = (self.d + 2 * i + 1) % m * w
                context.draw.line(context.screen, color, w1(position), w2(position), 1)
        self.d = (self.d + 1) % m

    def __str__(self):
        """Return the string representation of the object."""
        x = round(self.x, p)
        y = round(self.y, p)
        return "f(" + str(x) + "," + str(y) + ")"

    def getAbstract(self):
        """Return the object into its simple vector form."""
        return Vector(self.components)

    def setAbstract(self, vector):
        """Set the abstract vector to a new vector."""
        self.components = vector.components

    def delAbstract(self):
        """Set the abstract vector to null."""
        self.setNull()

    abstract = property(getAbstract, setAbstract, delAbstract, "Representation of the abstract vector of the force.")


class ForceField:
    def __init__(self, force, area):
        """Create a force field object."""
        self.force = force
        self.area = area

    def __contains__(self, body):
        """Determine if a body is contained in the force field."""
        # This function should be able to determine which proportion of the object is contained in the force
        # field in order to apply some of the force
        pass

    def exert(self, body):
        """Exert the force of the force field to the object."""
        pass


down = Vector([0, -1])
gravity = Force(0, -9.81, color=colors.RED)

if __name__ == "__main__":
    zero = Vector([0, 0])
    propulsion = Force(0, 0)
    o = Point.origin()

    random_force = Force.random()
    # print(random_force)
    random_force += gravity
    # print(random_force)

    result = Force.sum([gravity, propulsion, random_force])
    # print("Force.sum:",result)

    x, y = result
    # print(x,y) #Unpacking is compatible for vectors

    f = gravity
    print(result)

    from .context import Context

    context = Context()
    position = (0, 0)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        position = context.point()
        f.components = list(position)
        f.show(context, o)
        context.flip()
        # context.wait(0.1)
