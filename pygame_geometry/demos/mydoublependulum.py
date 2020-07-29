from mymanager import Manager
from mycurves import Trajectory
from mymotion import Motion
from myabstract import Vector

import random
import math

class Pendulum:
    @classmethod
    def random(cls, n=2):
        """Create a random pendulum."""
        angles = [Motion(math.pi*Vector.random(d=1), Vector.null(d=1),
                        Vector.null(d=1)) for i in range(n)]
        lengths = [random.uniform(0, 1) for i in range(n)]
        masses = [random.uniform(0, 1) for i in range(n)]
        return cls(angles, lengths, masses)

    def __init__(self, angles, lengths, masses, gravity=1):
        """Create a pendulum using the angles and the lengths."""
        self.angles = angles
        self.lengths = lengths
        self.masses = masses
        self.gravity = gravity

    def __str__(self):
        return "Pendulum(" + str(self.angles) + "," + str(self.lengths) + "," + str(self.masses) + ")"

    def show(self, context):
        """Show the pendulum."""
        self.trajectory.show(context)

    def update(self, dt):
        """Update the pendulum."""
        self.applySecondLawForTwo() #I want the general case
        self.updateAngles(dt)

    def applySecondLaw(self):
        """Apply the second law of mecanics to the angles."""
        g=self.gravity
        a0=self.angles[0].acceleration

    def applySecondLawForTwo(self):
        """Most naive implementation ever."""
        g=self.gravity
        m1,m2=self.masses
        l1,l2=self.lengths
        p1,v1=[a[0] for a in self.angles[0][:2]]
        p2,v2=[a[0] for a in self.angles[1][:2]]

        num=-g*(2*m1+m2)*math.sin(p1)-m2*g*math.sin(p1-2*p2)\
            -2*math.sin(p1-p2)*m2*(v2**2*l2+v1**2*l1*math.cos(p1-p2))
        den=l1*(2*m1+m2-m2*math.cos(2*p1-2*p2))
        self.angles[0].acceleration[0]=num/den

        num=2*math.sin(p1-p2)*(v1**2*l1*(m1+m2)+g*(m1+m2)*math.cos(p1)+\
            v2**2*l2*m2*math.cos(p1-p2))
        den=l2*(2*m1+m2-m2*math.cos(2*p1-2*p2))
        self.angles[1].acceleration[0]=num/den


    def updateAngles(self, dt):
        """Update the angles physically."""
        for angle in self.angles:
            angle.update(dt)

    @property
    def points(self):
        """Return the points of the pendulum."""
        angles_positions = [a.position[0] for a in self.angles]
        x, y = 0, 0
        points = [[x, y]]
        for angle, length in zip(angles_positions, self.lengths):
            x += length * math.sin(angle)
            y += -length * math.cos(angle)
            points.append([x, y])
        return points

    @property
    def trajectory(self):
        """Return the trajectory of the pendulum."""
        return Trajectory.createFromTuples(self.points)


class PendulumManager(Manager):
    @classmethod
    def random(cls, n=2):
        """Create a random pendulum."""
        return cls(Pendulum.random(n=2))

    def __init__(self, pendulum, name="Pendulum", dt=0.01):
        """Create a pendulum manager using the pendulum."""
        super().__init__(name=name)
        self.pendulum = pendulum
        self.dt = dt

    def update(self):
        """Update the pendulum."""
        self.pendulum.update(self.dt)

    def show(self):
        """Show the pendulum."""
        super().show()
        self.pendulum.show(self.context)


if __name__ == "__main__":
    pm = PendulumManager.random()
    pm()
