from mycase import Case
from random import randint
from myabstract import Vector,Point

import mycolors
import numpy as np
import math

class Entity:
    """Entity with 8 possible directions."""
    def __init__(self,x,y,r,mr=8):
        self.x=x
        self.y=y
        self.r=r
        self.mr=mr
    def __str__(self):
        return "Entity("+",".join(map(str,[self.x,self.y,self.r]))+")"
    def turnRight(self):
        self.r=(self.r+1)%self.mr
    def turnLeft(self):
        self.r=(self.r+self.mr-1)%self.mr
    def turnBack(self):
        self.r=(self.r+self.mr//2)%self.mr
    def stepForward(self,p=1):
        if self.r==0:
            self.x+=p
        elif self.r==1:
            self.x+=p
            self.y+=p
        elif self.r==2:
            self.y+=p
        elif self.r==3:
            self.x-=p
            self.y+=p
        elif self.r==4:
            self.x-=p
        elif self.x==5:
            self.x-=p
            self.y-=p
        elif self.r==6:
            self.y-=p
        else: #self.r==7
            self.x+=p
            self.y-=p
    def stepBackward(self,p=1):
        self.turnBack()
        self.stepForward(p)
        self.turnBack()
    def stepRigh(self):
        self.turnRight()
        self.stepForward()
    def stepLeft(self):
        self.turnLeft()
        self.stepForward()
    def getPosition(self):
        return [self.x,self.y]

    position=property(getPosition)

class BasicEntity(Case):
    """Defines a movable entity with 4 possible directions, a position, a size and a show method."""
    def __init__(self,*position,size=[1,1],direction=0,color=mycolors.WHITE,vector_color=mycolors.WHITE,vector_width=1,fill=True):
        """Create a basic entity."""
        if len(position)==1: position=position[0]
        self.position=list(position)
        self.size=size
        self.direction=direction
        self.color=color
        self.vector_color=vector_color
        self.vector_width=vector_width
        self.fill=fill


    def turnRight(self,n=1):
        """Turn right the direction of the basic entity."""
        self.direction=(self.direction+2+n)%4

    def turnLeft(self,n=1):
        """Turn left the direction of the basic entity."""
        self.direction=(self.direction+n)%4

    def turnBack(self,n=1):
        """Turn back the direction of the basic entity."""
        self.direction=(self.direction+2*n)%4

    def turnFront(self,n=1):
        """Turn front ?"""
        pass #It's useless to turn front just think a little...

    turn=turnBack #By default

    def update(self,n=1,direction=None):
        """Update the entity by changing the position according to the direction of the entity."""
        if not direction: direction=self.direction
        if direction==0:
            self.position[0]+=n
        if direction==1:
            self.position[1]+=n
        if direction==2:
            self.position[0]-=n
        if direction==3:
            self.position[1]-=n

    move=update

    def nextPosition(self,n=1,direction=None):
        """Return the next position of the entity according to its actual position and its direction."""
        if not direction: direction=self.direction
        position=self.position[:]
        if direction==0:
            position[0]+=n
        if direction==1:
            position[1]+=n
        if direction==2:
            position[0]-=n
        if direction==3:
            position[1]-=n
        return position

    def right(self):
        """Return the direction that correspond to the right of the entity."""
        return (self.direction+3)%4

    def left(self):
        """Return the direction that correspond to the left of the entity."""
        return (self.direction+1)%4

    def back(self):
        """Return the direction that correspond to the back of the entity."""
        return (self.direction+2)%4

    def front(self):
        """Return the direction that correspond to the front of the entity."""
        return self.direction

    def stepRight(self,n=1,r=1):
        """Make a step to the right."""
        self.turnRight(r)
        self.move(n)
        self.turnLeft(r)

    def stepLeft(self,n=1,r=1):
        """Make a step to the left."""
        self.turnLeft(r)
        self.move(n)
        self.turnRight(r)

    def stepBack(self,n=1,r=1):
        """Make a step back."""
        self.turnBack(r)
        self.move(n)
        self.turnBack(r)

    def stepForward(self,n=1):
        """Make a step forward."""
        self.move(n)

    def getAngle(self):
        """Return the angle corresponding to the direction."""
        return self.direction*math.pi*2

    def setAngle(self,angle):
        """Set the angle corresponding to the direction."""
        self.direction=int(angle/math.pi/2)

    def getVector(self):
        """Return the direction vector."""
        around=[(1,0),(0,1),(-1,0),(0,-1)]
        return Vector(around[self.direction])

    def setVector(self,vector):
        """Set the vector of the entity."""
        x,y=vector
        around=[(1,0),(0,1),(-1,0),(0,-1)]
        self.direction=around.index((x,y))

    def getPoint(self):
        """Return the associated point."""
        return Point(self.position)

    def setPoint(self,point):
        """Set the point of the entity."""
        self.position=point.position

    vector=property(getVector,setVector,"Allow the user to manipulate the vector of the entity easily.")
    angle=property(getAngle,setAngle,"Allow the user to manipulate the angle of the entity easily.")
    #point=property(getPoint,setPoint,"Allow the user to manipulate the point of the entity easily.")

    def showVector(self,context,color=None,width=None):
        """Show the direction vector of the entity."""
        if not color: color=self.vector_color
        if not width: width=self.vector_width
        self.vector.show(context,self.center,color=color,width=width)

    def show(self,context,**kwargs):
        """Show the case. By default it only show the associated form."""
        self.showForm(context,**kwargs)
        self.showVector(context,**kwargs)

class BasicRayEntity(BasicEntity):
    def __init__(self,*position,size=[1,1],direction=0,view=math.pi/2,nrays=10,color=mycolors.WHITE,vector_color=mycolors.WHITE,vector_width=1,fill=True):
        """Create a basic entity."""
        if len(position)==1: position=position[0]
        self.position=list(position)
        self.size=size
        self.direction=direction
        self.color=color
        self.vector_color=vector_color
        self.vector_width=vector_width
        self.fill=fill
        self.nrays=nrays

    def getRays(self):
        """Return the rays emited by the entity."""
        vmin=-self.view/2
        vmax=self.view/2
        a=self.angle
        return [Ray(self.position,d) for d in np.linspace(a+vmin,a+vmax,self.nrays)]






class Maze:
    """Uses the zone and eller's algorithms in order to show a solvable maze."""
    def conversion(M,l,nl):
        """Convert the elements l of the matrix M by the elements of nl."""
        if type(M[0])==list:
            for i in range(len(M)):
                M[i]=Maze.conversion(M[i],l,nl)
        else:
            for i in range(len(M)):
                M[i]=nl[l.index(M[i])]
        return M


    def convert(maze):
        """Convert the caracterization of the eller's maze into a more visible one."""
        pretty_maze = [["X"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        for y,row in enumerate(maze):
            for x,col in enumerate(row):
                pretty_maze[2*y+1][2*x+1] = " "
                for direction in col:
                    pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = " "
        return pretty_maze

    def make_empty_grid(width, height):
        """Create a empty grid using its width and height."""
        return [[[] for x in range(width)] for y in range(height)]

    def eller(maze):
        """Return the caracterization of the eller's maze."""
        sets = list(range(len(maze[0])))
        for y, row in enumerate(maze):
            for x, col in enumerate(row[:-1]):
                if ((row == maze[-1] or randint(0,1)) and sets[x] != sets[x+1]):
                    sets[x+1] = sets[x]
                    maze[y][x].append((0,1))
                    maze[y][x+1].append((0,-1))
            if row != maze[-1]:
                next_sets = list(range(y*len(maze[0]), (y+1)*len(maze[0])))
                all_sets = set(sets)
                have_moved = set()
                while all_sets != have_moved:
                    for x, col in enumerate(row):
                        if randint(0,1) and sets[x] not in have_moved:
                            have_moved.add(sets[x])
                            next_sets[x] = sets[x]
                            maze[y][x].append((1,0))
                            maze[y+1][x].append((-1,0))
                sets = next_sets
        return maze

    def __init__(self,matrix,position=[0,0],fill=True):
        """Create a maze using size."""
        self.position=position
        self.fill=fill
        self.matrix=matrix

    def getSize(self):
        """Return the size of the maze."""
        return np.shape(self.matrix)

    def setSize(self,size):
        """Set the size of the maze."""
        sx,sy=size
        self.matrix=self.matrix[:sy][:sx]

    def getCases(self,fill=None):
        """Return all the cases that correspond to 1 on the matrix of the maze."""
        if not fill: fill=self.fill
        sx,sy=self.size
        px,py=self.position
        return [Case(x+px,y+py,fill=fill) for x in range(sx) for y in range(sy) if self.matrix[y][x]]

    def show(self,surface):
        """Show the maze on the surface."""
        xmin,ymin,xmax,ymax=surface.corners
        sx,sy=self.size
        for case in self.getCases():
            case.show(surface)

    def available(self,*position):
        """Determine if a position is available or not."""
        if len(position)==1: position=position[0]
        x,y=position
        return self.matrix[y][x]==0

    size=property(getSize,setSize,"Allow the user to manipulate the size of the maze easily.")

class Solver:
    """Solves a maze using the 'always turn right' method."""
    def __init__(self,maze,entity):
        """Create a solver unsing the maze and an entity."""
        self.maze=maze
        self.entity=entity

    def update(self):
        """Move the entity of one step."""
        if self.lookRight():
            self.entity.turnRight()
        if self.lookFront():
            self.entity.update()
        else:
            self.entity.turnLeft()

    def lookRight(self):
        """Determine if the case of the maze at the right of the entity is available."""
        self.entity.stepRight()
        available=self.maze.available(self.entity.position)
        self.entity.stepLeft()
        return available

    def lookLeft(self):
        """Determine if the case of the maze at the left of the entity is available."""
        self.entity.stepLeft()
        available=self.maze.available(self.entity.position)
        self.entity.stepRight()
        return available

    def lookFront(self):
        """Determinei if the case of the maze at the front of the entity is available."""
        return self.maze.available(self.entity.nextPosition())



    def getAvailableDirections(self):
        """Return the list of available positions."""
        x,y=self.entity.position
        return [int(self.maze.available(x+dx,y+dy)) for (dx,dy) in self.getAround()]

    def getAround(self):
        """Return the 4 directions."""
        return [(1,0),(0,1),(-1,0),(0,-1)]

    def show(self,context):
        """Show the maze and the entity."""
        self.maze.show(context)
        self.entity.show(context)

    def showVision(self,context):
        """Show the 'vision' of the entity."""
        self.entity.show(context)
        for segment in self.getCollidedRays():
            segment.show(context)

    def getCollidedRays(self):
        """Stop the rays on the objects to return resulting segments."""
        new_rays=[]
        for ray in self.entity.getRays():
            for form in self.forms:
                new_rays.append(ray.crossForm(form))
                break
        return new_rays



if __name__=="__main__":
    from myzone import Zone
    from mycontext import Context
    s=20
    size=[s,s]
    zone=Zone([2*s,2*s])
    context=Context(name="Maze",fullscreen=True)
    matrix=np.array(Maze.conversion(Maze.convert(Maze.eller(Maze.make_empty_grid(*size))),['X',' '],[1,0]))
    maze=Maze(matrix,fill=True)
    entity=BasicEntity(1,1,color=mycolors.RED,vector_color=mycolors.GREEN,vector_width=3)
    solver=Solver(maze,entity)
    n=0
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        n=(n+1)%1
        if n==0:
            solver.update()
        solver.show(context)
        context.flip()
