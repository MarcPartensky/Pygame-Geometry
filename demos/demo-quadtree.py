from pygame_geometry.quadtree import QuadTree
from pygame_geometry.manager import Manager
from pygame_geometry.motion import Motion
from pygame_geometry.abstract import Point

import time

class QuadtreeManager(Manager):
    @classmethod
    def random(cls,n=50):
        """Create a quadtree of 'n' points."""
        return cls(QuadTree.random(n=n))

    def __init__(self,quadtree,name="Quadtree Manager"):
        """Create a quadtree manager using the quadtree."""
        super().__init__(name=name)
        self.quadtree=quadtree
        self.quadtree.compute()

    def show(self):
        """Show the quadtree."""
        self.quadtree.show(self.context)

class QuadtreeTester(Manager):
    @classmethod
    def random(cls,n=50,**kwargs):
        """Create a quadtree of 'n' points."""
        motions=[Motion.random(n=2) for i in range(n)]
        return cls(motions,**kwargs)

    def __init__(self,motions,name="Quadtree Manager",**kwargs):
        """Create a quadtree manager using the quadtree."""
        super().__init__(name=name,**kwargs)
        self.motions=motions

    def update(self):
        """Update the motions and in consequence the quadtree."""
        self.updateMotions()
        self.quadtree=QuadTree(self.points)
        self.quadtree.compute()

    def updateMotions(self):
        """Update the motions."""
        for motion in self.motions:
            motion.update(self.dt)

    def show(self):
        """Show the quadtree."""
        self.quadtree.show(self.context)

    @property
    def points(self):
        """Return the points at the positions of the motions."""
        return [Point(*m.position) for m in self.motions]

t=time.time()
qm=QuadtreeTester.random(n=200,fullscreen=True)
qm()
print(time.time()-t)

