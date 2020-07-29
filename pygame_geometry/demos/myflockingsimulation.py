from mymanager import Manager
from myabstract import Vector, Form, Circle
from mymotion import Motion
from mybody import Body
import mycolors
import math


class Boid(Body):
    """Representation of a boid of craig reynolds."""

    @classmethod
    def random(cls, p=100, v=10):
        """Create a boid with a random motion."""
        p = p * Vector.random()
        v = v * Vector.random()
        a = Vector.null()
        m = Motion(p, v, a)
        return cls(m)

    def __init__(self, motion,
                 max_velocity=2,
                 max_acceleration=4,
                 alignment_perception=10,
                 cohesion_perception=10,
                 separation_perception=2,
                 alignment_influence=10,
                 cohesion_influence=10,
                 separation_influence=10,
                 **kwargs
                 ):
        """Create a boid."""
        anatomy = self.makeAnatomy(**kwargs)
        print(list(map(str,anatomy.points)))
        print(anatomy.area)
        print(anatomy.center)
        super().__init__(anatomy, motion)
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.alignment_perception = alignment_perception
        self.cohesion_perception = cohesion_perception
        self.separation_perception = separation_perception
        self.alignment_influence = alignment_influence
        self.cohesion_influence = cohesion_influence
        self.separation_influence = separation_influence

    def makeAnatomy(self, **kwargs):
        """Return the anatomy of a boid."""
        if not "area_color" in kwargs:
            kwargs["area_color"] = mycolors.RED
        if not "fill" in kwargs:
            kwargs["fill"] = True
        anatomy = Form.createFromTuples([(1, 0), (-1, -1), (-0.5, 0), (-1, 1)], **kwargs)
        anatomy.recenter()
        return anatomy

    def getVisibleMates(self, mates, perception):
        """Return all mates within the perception radius."""
        visible_mates = []
        for mate in mates:
            v = mate.position - self.position
            if v.norm < perception:
                visible_mates.append(mate)
        return visible_mates

    def updateAlignment(self, mates):
        """Alignment: Steer towards the average heading of local flockmates."""
        #mates = self.getVisibleMates(mates, self.alignment_perception)
        if len(mates) == 0:
            return Vector.null()
        v = Vector.average([m.velocity for m in mates])
        v.norm = self.max_velocity
        v -= self.velocity
        v.limit(self.max_acceleration)
        return v

    def updateCohesion(self, mates):
        """Cohesion: steer to move toward the average position of local
        flockmates."""
        #mates = self.getVisibleMates(mates, self.cohesion_perception)
        if len(mates) == 0:
            return Vector.null()
        p = Vector.average([m.position for m in mates])
        v = p - self.position
        v.norm = self.max_velocity
        v -= self.velocity
        v.limit(self.max_acceleration)
        return v

    def updateSeparation(self, mates):
        """Separation: Avoid crowding local flockmates."""
        #mates = self.getVisibleMates(mates, self.separation_perception)
        if len(mates) == 0:
            return Vector.null()
        vs = []
        for mate in mates:
            v = self.position - mate.position
            v.norm = 1 / v.norm
            vs.append(v)
        v = Vector.average(vs)
        v.norm = self.max_velocity
        v -= self.velocity
        v.limit(self.max_acceleration)
        return v

    def updateRules(self, mates):
        """Update the boid with the rules they obbey."""
        vs = []
        i1 = self.alignment_influence
        i2 = self.cohesion_influence
        i3 = self.separation_influence
        v1 = self.updateAlignment(mates)
        v2 = self.updateCohesion(mates)
        v3 = self.updateSeparation(mates)
        v = (i1 * v1 + i2 * v2 + i3 * v3) / (i1 + i2 + i3)
        # self.acceleration.set(v)
        return v

    def updateLimit(self, born):
        """Update the position of the boid in order to stay in the born."""
        p = self.position
        if self.position.norm > born:
            p *= -0.9
        return p

    def updateFriction(self, friction):
        """Add some friction to the body."""
        return self.velocity * (1 - friction)

    def update(self, dt, mates, friction, born):
        """Update with friction."""
        super().update(dt)
        v = self.updateFriction(friction)
        a = self.updateRules(mates)
        p = self.updateLimit(born)
        return Motion(p, v, a)


class BoidGroup:
    @classmethod
    def random(cls, n=10):
        """Create a group of random boids."""
        boids = [Boid.random() for i in range(n)]
        return BoidGroup(boids)

    def __init__(self, boids, mates_number=3, mates_radius=10):
        """Create a boid group using boids."""
        self.boids = boids
        self.mates_number = mates_number
        self.mates_radius = mates_radius

    def show(self, context):
        """Show the object."""
        for boid in self.boids:
            boid.show(context)

    def showMotions(self, context):
        """Show the motions of the objects."""
        for boid in self.boids:
            boid.showMotion(context)

    def update(self, dt, friction, born):
        """Update the object."""
        motions = []
        for i in range(len(self.boids)):
            mates = self.getMates(i)
            motion = self.boids[i].update(dt, mates, friction, born)
            motions.append(motion)

        for i in range(len(self.boids)):
            self.boids[i].motion.set(motions[i])

    def getMates(self, j):
        """Return the local mates of boid 'i'."""
        mates = []
        bj = self.boids[j]
        for i in range(len(self.boids)):
            if i != j:
                bi = self.boids[i]
                p = bj.position - bi.position
                if p.norm < self.mates_radius:
                    mates.append(bi)
        return mates

    def updateEach(self, dt, friction):
        """Update each boid individually."""
        for boid in self.boids:
            boid.update(dt, friction)

    def follow(self, point):
        """Follow the given point."""
        p=Vector(*point)
        for boid in self.boids:
            v=(p-boid.position)/10
            print(v,boid.acceleration)
            boid.acceleration.set(boid.acceleration+v)
            print(boid.acceleration)

    def adjustVelocities(self):
        """Adjust the velocity of each boid to the one of its neighbours."""
        for i in range(len(self.boids)):
            neighbours = self.getNeighbours(i)
            self.boids[i].adjustVelocity(neighbours)

    def getNeighbours(self, j):
        """Return the neighbours of the b-th boid."""
        proximity = [(self.distance(i, j), i) for i in range(len(self.boids))]
        proximity.sort(key=lambda x: x[0])
        proximity = proximity[:self.neighbours_number]
        neighbours = [self.boids[p[1]] for p in proximity]
        return neighbours

    def distance(self, i, j):
        """Return the distance between the boids i and j."""
        p1 = self.boids[i].position
        p2 = self.boids[j].position
        return (p1 - p2).norm


class Simulation(Manager):
    @classmethod
    def random(cls, n=20, **kwargs):
        """Create a random simulation of boids."""
        return cls(BoidGroup.random(n), **kwargs)

    def __init__(self, group, friction=1e-3, radius=100, dt=1, **kwargs):
        """Create a simulation of flocking."""
        super().__init__(dt=dt, **kwargs)
        self.group = group
        self.friction = friction
        self.circle = Circle(0,0, radius=radius)

    def update(self):
        """Update the boid group."""
        self.group.update(self.dt, self.friction, self.circle.radius)
        # self.group.follow(self.context.point())

    def show(self):
        """Show the boid group."""
        self.group.show(self.context)
        self.group.showMotions(self.context)
        self.circle.show(self.context)


if __name__ == "__main__":
    s = Simulation.random(n=40)
    s()
