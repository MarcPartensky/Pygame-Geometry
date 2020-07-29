from .abstract import Segment, Vector, Line
from .anatomies import CircleAnato, FormAnatomy
from .manager import Manager
from .motion import Motion, Moment
from .entity import Entity
from .rectangle import Square
from .group import Group

import math


# class DeprecatedCollider:
#     def __call__(self, entity1, entity2):
#         if (entity1.position-entity2.position).norm < entity1.anatomy.radius + entity2.anatomy.radius:
#             x1, y1 = entity1.position
#             x2, y2 = entity2.position
#             m1 = entity1.mass
#             m2 = entity2.mass
#             if x2 != x1:
#                 angle = -math.atan((y2 - y1) / (x2 - x1))
#                 ux1, uy1 = self.rotate(entity1.velocity, angle)
#                 ux2, uy2 = self.rotate(entity2.velocity, angle)
#                 v1 = Vector(self.project(ux1, ux2, m1, m2), uy1)
#                 v2 = Vector(self.project(ux2, ux1, m1, m2), uy2)
#                 entity1.velocity = self.rotate(v1, -angle)
#                 entity2.velocity = self.rotate(v2, -angle)
#
#     def project(self, v1, v2, m1, m2):
#         return (m1 - m2) / (m1 + m2) * v1 + (2 * m2) / (m1 + m2) * v2
#
#     def rotate(self, velocity, angle):
#         vx, vy = velocity
#         nvx = vx * math.cos(angle) - vy * math.sin(angle)
#         nvy = vx * math.sin(angle) + vy * math.cos(angle)
#         return [nvx, nvy]


# class CircleCollider(Collider):
#     def cross(self, e1, e2):
#         vector = e1.position - e2.position
#         radius = e1.anatomy.radius + e2.anatomy.radius
#         if vector.norm < radius:
#             v1 = -e1.anatomy.radius * vector.unit
#             v2 = e2.anatomy.radius * vector.unit
#             p1 = v1(e1.position)
#             p2 = v2(e2.position)
#             s = Segment(p1, p2)
#             return s.middle

    # def collide(self, e1, e2):
    #     """Determine whether there is a collision or not."""
    #     vector = e1.position - e2.position
    #     radius = e1.anatomy.radius + e2.anatomy.radius
    #     return vector.norm < radius


# class EntityCollider1(Collider):
#     def bump(self, e1, e2):
#         # We redirect the velocities
#         tangent = math.atan2(e2.y - e1.y, e2.x - e1.x)
#         e1.velocity.angle = 2 * tangent - e1.velocity.angle
#         e2.velocity.angle = 2 * tangent - e2.velocity.angle
#         e1.velocity.norm, e2.velocity.norm = e2.velocity.norm, e1.velocity.norm


# class EntityCollider2(Collider):
#     def bump(self, e1, e2):
#         # We redirect the velocities
#         angle = math.atan2(e2.y - e1.y, e2.x - e1.x)
#         e1.velocity.angle = -angle
#         e2.velocity.angle = angle
#         mass = e1.mass + e2.mass
#         velocity = e1.velocity + e2.velocity
#         e1_velocity_norm = (velocity.norm * mass - e2.velocity.norm * e2.mass) / e1.mass
#         e2_velocity_norm = (velocity.norm * mass - e1.velocity.norm * e1.mass) / e2.mass
#         e1.velocity.norm = e1_velocity_norm
#         e2.velocity.norm = e2_velocity_norm

        # pm = p1 + p2
        # v*m = v1*m1 + v2*m2
        # v1 = (v*m - v2*m2) / m1


class Collider:
    def __init__(self, elasticity=1e-5):
        self.elasticity = elasticity

    def soloChocs(self, g, **kwargs):
        l = g.flattened()
        for (i, e1) in enumerate(l):
            for e2 in l[i+1:]:
                if self.collide(e1, e2):
                    self.bump(e1, e2, **kwargs)

    def multiChocs(self, g1, g2, **kwargs):
        for (i, e1) in enumerate(g1.flattened()):
            for e2 in g2.flattened():
                if self.collide(e1, e2):
                    self.bump(e1, e2, **kwargs)

    __call__ = multiChocs

    def collide(self, e1, e2):
        """Determine if their is a collision or not."""
        vector = e1.position - e2.position
        radius = e1.anatomy.born + e2.anatomy.born
        if vector.norm < radius:
            return e1.collide(e2)
        return False

    def cross(self, e1, e2):
        """Determine the point of collision."""
        points = e1.cross(e2)
        p1, p2 = points
        s = Segment(p1, p2)
        l = Line(s.middle, s.angle+math.pi/2)
        pts1 = l.projectPoints(e1.points)
        pts2 = l.projectPoints(e2.points)
        pass

    def correctOverlapping(self, e1, e2):
        # We correct the overlapping
        tangent = math.atan2(e2.y - e1.y, e2.x - e1.x)
        vector = e1.position - e2.position
        radius = e1.anatomy.born + e2.anatomy.born
        r = (vector.norm - radius) / 2
        angle = 0.5 * math.pi + tangent
        e1.x += r * math.sin(angle)
        e1.y -= r * math.cos(angle)
        e2.x -= r * math.sin(angle)
        e2.y += r * math.cos(angle)

    def applyElasticity(self, e):
        """Apply some elasticity on the collision."""
        e.velocity.norm *= self.elasticity

    def bump(self, e1, e2,
             hitting=False, hitting1=False, hitting2=False,
             killing=False, killing1=False, killing2=False,
             bouncing=False, bouncing1=False, bouncing2=False,
             overlapping=False, overlapping1=False, overlapping2=False,
             elastic=False, elastic1=False, elastic2=False,
             ):
        if hitting1 or hitting:
            e1.hit(e2)
        if hitting2 or hitting:
            e2.hit(e1)
        if killing1 or killing:
            e1.die()
        if killing2 or killing:
            e2.die()
        if bouncing1 or bouncing:
            self.bounce(e1, e2)
        if bouncing2 or bouncing:
            self.bounce(e2, e1)
        if overlapping1 or overlapping:
            self.correctOverlapping(e1, e2)
        if overlapping2 or overlapping:
            self.correctOverlapping(e2, e1)
        if elastic1 or elastic:
            self.applyElasticity(e1)
        if elastic2 or elastic:
            self.applyElasticity(e2)

    def bounce(self, e1, e2):
        """Make e1 and e2 bounce one upon another."""
        v1 = (e1.mass - e2.mass) / (e1.mass + e2.mass) * e1.velocity + \
             (2 * e2.mass) / (e1.mass + e2.mass) * e2.velocity
        # v2 = (e2.mass - e1.mass) / (e1.mass + e2.mass) * e2.velocity + \
        #      (2 * e1.mass) / (e1.mass + e2.mass) * e1.velocity
        e1.velocity.set(v1)
        # e2.velocity.set(v2)



class ColliderTester(Manager):
    def __init__(self, n=10, s=5, g=10, radius_borns=[1, 10], **kwargs):
        super().__init__(**kwargs)
        # entities = [Entity(FormAnatomy.random(),
        #             [Motion(s * Vector.random(), 10 * Vector.random(), Vector(0, -g)),
        #              Moment(Vector.random(), 5*Vector.random())], friction=0)
        #             for i in range(n)]
        self.group = Group(*[Entity(CircleAnatomy.random(radius_borns=radius_borns), \
                            [Motion(s*Vector.random(), Vector(0,0), Vector(0, -g))], friction=0.1) \
                            for i in range(n)])
        self.collider = Collider(elasticity=0.9)
        self.born = s
        self.born_elasticity = 0.5
        self.square = Square(0, 0, 2 * self.born)
        self.correctMasses()

    def correctMasses(self):
        for entity in self.group:
            entity.mass = entity.anatomy.area

    def update(self):
        super().update()
        for e in self.group:
            e.update(self.dt)
        self.collider.soloChocs(self.group, bouncing=True, overlapping=True, elastic=True)
        for e in self.group:
            self.limit(e)

        self.context.camera.write()

    def show(self):
        super().show()
        self.showGroup()
        self.square.show(self.context)

    def showGroup(self):
        for e in self.group:
            e.show(self.context)

    def limit(self, e):
        l = self.born_elasticity
        r = e.born
        if e.x > self.born - r:
            e.x = self.born - r
            e.vx *= -l
        if e.x < -self.born + r:
            e.x = -self.born + r
            e.vx *= -l
        if e.y > self.born - r:
            e.y = self.born - r
            e.vy *= -l
        if e.y < -self.born + r:
            e.y = -self.born + r
            e.vy *= -l


if __name__ == "__main__":
    m = ColliderTester(n=100, s=5, dt=0.001, radius_borns=[0.15, 0.2], fullscreen=True)
    m.context.camera.buildScreenWriter("Sand Simulation.mp4", framerate=100)
    m()
    m.context.camera.release()
