from collections import namedtuple
from .abstract import Point
from . import colors
from functools import reduce


import numpy as np

import operator
import random
import math
import copy


from tools import timer
#Point = namedtuple('Point', ['x', 'y'])


def randomPoint():
    return Point(random.uniform(-1, 1), random.uniform(-1, 1))

def randintPoint():
    return Point(random.randint(-10, 10), random.randint(-10, 10))

n = 10
points = [randomPoint() for i in range(n)]


class QuadTree:
    @classmethod
    def random(cls,n,**kwargs):
        """Create a quadtree of 'n' points."""
        points = [Point.random() for i in range(n)]
        return cls(points,**kwargs)


    def __init__(self, points,
                 neighbors=1,
                 color=colors.WHITE,
                 depth=float('inf')):
        """Create a quadtree using its positions."""
        self.check(points)
        self.points = dict(zip(range(len(points)), points))
        self.neighbors = neighbors
        self.color = color
        self.depth = depth

    def check(self, points):
        """Determine the points are one upon another."""
        pts=[tuple(p) for p in points]
        if sorted(list(set(pts))) != sorted(pts):
            raise Exception("No point must be upon another.")

    def compute(self):
        """Compute all objects."""
        self.position = self.computePosition()
        self.length = self.computeLength()
        self.paths = {}
        self.tree = self.computeDictTree(self.points, self.position, self.length)

    def computePosition(self):
        """Compute the position of the quadtree."""
        xmin = min([p.x for p in self.points.values()])
        xmax = max([p.x for p in self.points.values()])
        ymin = min([p.y for p in self.points.values()])
        ymax = max([p.y for p in self.points.values()])
        x = (xmax + xmin) / 2
        y = (ymax + ymin) / 2
        return [x, y]

    def computeLength(self):
        """Compute the length of the quadtree."""
        xmin = min([p.x for p in self.points.values()])
        xmax = max([p.x for p in self.points.values()])
        ymin = min([p.y for p in self.points.values()])
        ymax = max([p.y for p in self.points.values()])
        return max(xmax - xmin, ymax - ymin)

    def __str__(self):
        return "QuadTree("+str(self.getDictionary(self.tree))+")"

    def computeDictTree(self, points, position, length, n=0, path=[]):
        """Find the sub trees."""
        if len(points) == 0:
            return None
        elif len(points) <= self.neighbors or n > self.depth:
            for key in points:
                self.paths[key] = path
            return list(points.keys())
        else:
            x, y = position
            l = length
            pos1 = (x - l / 4, y + l / 4)
            pos2 = (x + l / 4, y + l / 4)
            pos3 = (x - l / 4, y - l / 4)
            pos4 = (x + l / 4, y - l / 4)
            pts1, pts2, pts3, pts4 = [], [], [], []

            for key, pt in points.items():
                if pt.x > x:
                    if pt.y > y:
                        pts2.append((key, pt))
                    else:
                        pts4.append((key, pt))
                else:
                    if pt.y > y:
                        pts1.append((key, pt))
                    else:
                        pts3.append((key, pt))

            pts1 = dict(pts1)
            pts2 = dict(pts2)
            pts3 = dict(pts3)
            pts4 = dict(pts4)

            tree={}
            t0=self.computeDictTree(pts1, pos1, l/2, n+1, path+[0])
            t1=self.computeDictTree(pts2, pos2, l/2, n+1, path+[1])
            t2=self.computeDictTree(pts3, pos3, l/2, n+1, path+[2])
            t3=self.computeDictTree(pts4, pos4, l/2, n+1, path+[3])
            if t0: tree[0]=t0
            if t1: tree[1]=t1
            if t2: tree[2]=t2
            if t3: tree[3]=t3
            return tree

    def getDictFromList(self,tree):
        """Return the tree under the dictionary syntax using the tree in
        the None syntax."""
        cdb=True
        for e in tree:
            if isinstance(e,list):
                cdb=False
        if cdb:
            return tree
        else:
            d={}
            for i,e in enumerate(tree):
                if e is not None:
                    d[i]=self.getDictFromList(e)
            return d

    def computeListTree(self, points, position, length, n=0, path=[]):
        """Find the sub trees."""
        if len(points) == 0:
            return None
        elif len(points) <= self.neighbors or n > self.depth:
            for key in points:
                self.paths[key] = path
            return list(points.keys())
        else:
            x, y = position
            l = length
            pos1 = (x - l / 4, y + l / 4)
            pos2 = (x + l / 4, y + l / 4)
            pos3 = (x - l / 4, y - l / 4)
            pos4 = (x + l / 4, y - l / 4)
            pts1, pts2, pts3, pts4 = [], [], [], []

            for key, pt in points.items():
                if pt.x > x:
                    if pt.y > y:
                        pts2.append((key, pt))
                    else:
                        pts4.append((key, pt))
                else:
                    if pt.y > y:
                        pts1.append((key, pt))
                    else:
                        pts3.append((key, pt))

            pts1 = dict(pts1)
            pts2 = dict(pts2)
            pts3 = dict(pts3)
            pts4 = dict(pts4)

            return [self.computeListTree(pts1, pos1, l/2, n+1, path+[0]),
                    self.computeListTree(pts2, pos2, l/2, n+1, path+[1]),
                    self.computeListTree(pts3, pos3, l/2, n+1, path+[2]),
                    self.computeListTree(pts4, pos4, l/2, n+1, path+[3])]

    def getSquare(self):
        """Return all the squares of the paths."""
        squares=[]
        for path in self.paths:
            length=self.length/2**len(path)
            l=self.length
            x,y=self.position
            for level in path:
                if level==0:
                    x-=l/level
                    y+=l/level
                elif level==1:
                    x+=l/level
                    y+=l/level
                elif level==2:
                    x-=l/level
                    y-=l/level
                else:
                    x+=l/level
                    y-=l/level
            squares.append(((x,y),length))
        return squares

    def show(self,context):
        """Show the quadtree."""
        self.showTree(context,self.tree,self.position,self.length/2)
        self.showPoints(context)

    def showPoints(self,context):
        """Show each point."""
        for point in self.points.values():
            point.show(context)

    def showTree(self,context,tree,position,length):
        """Show the given trees recusively."""
        #Unpack the values
        x,y=position
        l=length
        #Show a square
        points=[(x-l,y+l),(x+l,y+l),(x+l,y-l),(x-l,y-l)]
        context.draw.lines(context.screen,self.color,points)
        if isinstance(tree,list):
            if tree[0]: self.showTree(context,tree[0],(x-l/2,y+l/2),l/2)
            if tree[1]: self.showTree(context,tree[0],(x+l/2,y+l/2),l/2)
            if tree[2]: self.showTree(context,tree[0],(x-l/2,y-l/2),l/2)
            if tree[3]: self.showTree(context,tree[0],(x+l/2,y-l/2),l/2)

    def showDictionary(self,context,tree,position,length):
        """Show the given trees recusively."""
        #Unpack the values
        x,y=position
        l=length
        #Show a square
        points=[(x-l,y+l),(x+l,y+l),(x+l,y-l),(x-l,y-l)]
        context.draw.lines(context.screen,self.color,points)
        if isinstance(tree,dict):
            #Show the trees
            if 0 in tree:
                self.showTree(context,tree[0],(x-l/2,y+l/2),l/2)
            if 1 in tree:
                self.showTree(context,tree[1],(x+l/2,y+l/2),l/2)
            if 2 in tree:
                self.showTree(context,tree[2],(x-l/2,y-l/2),l/2)
            if 3 in tree:
                self.showTree(context,tree[3],(x+l/2,y-l/2),l/2)

    def isCircleCrossingSquare(self,square,circle):
        """Detect the collision of a square and a circle."""
        qx,qy,qr=square
        cx,cy,cr=circle
        return abs(qx-cx)<=qr/2+cr and abs(qy-cy)<=qr/2+cr

    def isCircleInSquare(self,square,circle):
        """Detect the collision of a square and a circle."""
        qx,qy,qr=square
        cx,cy,cr=circle
        return abs(qx-cx)<=qr/2-cr and abs(qy-cy)<=qr/2-cr

    def extractAll(self,radiuses):
        """All the collisions occuring in the quadtree."""


    def extract(self,index,radius):
        """Extract the points that are in the circle of center the point of
        index 'index' and of radius 'radius' using the quadtree map."""
        circle=(*self.points[index],radius)
        path=self.paths[index]
        path=self.rise(circle,path)
        square=self.getSquare(path)
        tree=self.access(path)
        points=self.fall(tree,path,circle,square)
        return points

    def rise(self,circle,path):
        """Return the deepest square path that borns the circle."""
        square=self.getSquare(path)
        while not self.isCircleInSquare(square,circle) and len(path)>0:
            path=path[:-1]
            square=self.getSquare(path)
        return path

    def fall(self,tree,path,circle,square):
        """Return the points that are in the circle using the path recursively."""
        print(tree)
        if isinstance(tree,list):
            points=[]
            for i in tree:
                x,y=self.points[i]
                cx,cy,cr=circle
                if (x-cx)**2+(y-cy)**2<=cr**2:
                    #points.append((x,y))
                    points.append(i)
            return points
        else:
            x,y,l=square
            points=[]
            for (k,t) in tree.items():
                if k==0: square=(x-l/2,y+l/2,l/2)
                elif k==1: square=(x+l/2,y+l/2,l/2)
                elif k==2: square=(x-l/2,y-l/2,l/2)
                elif k==3: square=(x+l/2,y-l/2,l/2)
                if self.isCircleCrossingSquare(circle,square):
                    points+=self.fall(t,path+[k],circle,square)
            return points

    def getSquare(self,path):
        """Return the square of a given path."""
        x,y=0,0
        n=len(path)
        l=self.length/2**n
        for i in range(n):
            d=l/2**i
            m=path[i]
            if m==0:
                x-=d
                y+=d
            elif m==1:
                x+=d
                y+=d
            elif m==2:
                x-=d
                y-=d
            else:
                x+=d
                y-=d
        return (x,y,l)

    def access(self,path):
        """Return the tree filled accessed by the path."""
        return reduce(operator.getitem, path, self.tree)

    def flatten(self,tree):
        """Unload the components of a given tree."""
        return l

    def extractWithCircles(self,index,radius):
        """Extract the points that are in the circle of index 'index' and
        radius 'radius'."""
        cx,cy=self.points[index]
        n=len(self.points)
        points=[]
        for i in range(n):
            if i!=index:
                x,y=self.points[i]
                if (x-cx)**2+(y-cy)**2<=radius**2:
                    #points.append((x,y))
                    points.append(i)
        return points


if __name__ == "__main__":
    from .manager import Manager
    from .motion import Motion

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
    # n=500
    # q=QuadTree.random(n=n)
    # q.compute()
    # print(q.tree)
    # p=q.paths[0]
    # print(p)
    # i=q.access(p)
    # print(i)
    # sq=q.getSquare(p)
    # print(sq)
    # r=q.length*2
    # m=4
    # t0=time.time()
    # proximities=[]
    # for i in range(4):
    #     proximities.append(q.extract(i,r))
    #     print("")
    #     # c=(*q.points[i],r)
    #     # sq=q.getSquare(q.paths[i])
    #     # pts=q.fall(q.tree,[],c,sq)
    #     # proximities.append(pts)
    # print(len(proximities[0]))
    # print(time.time()-t0)
    # print('\n')
    #
    # t0=time.time()
    # proximities=[]
    # for i in range(4):
    #     proximities.append(q.extractWithCircles(i,r))
    # print(len(proximities[0]))
    # print(time.time()-t0)
