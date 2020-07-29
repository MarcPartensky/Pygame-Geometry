from mypixel import Pixel
from pygame.locals import *

import mycolors

class GameOfLife:
    """Uses the plan to display."""
    def __init__(self,cases=[]):
        """Create a game of life object."""
        self.cases=cases
        self.on=0

    def __call__(self,surface):
        """Execute the main loop."""
        while surface.open:
            surface.check()
            surface.control()
            surface.clear()
            surface.show()
            self.control(surface)
            self.update()
            self.show(surface)
            surface.flip()


    def show(self,surface):
        """Show the game of life on the surface."""
        pixel=Pixel()
        for position in self.cases:
            pixel.show(surface,position)

    def fastShow(self,surface):
        """Show the game of life on the surface 10 times faster."""
        for (x,y) in self.cases:
            surface.draw.rect(surface.screen,mycolors.WHITE,[x,y,1,1],0)


    def control(self,surface):
        """Control the game of life."""
        click=surface.click()
        keys=surface.press()
        if keys[K_SPACE]:
            self.on=(self.on+1)%2
        if not click: return
        cursor=surface.point()
        case=tuple([round(cursor[i]-1/2) for i in range(2)])
        if not self.hasCase(case):
            self.addCase(case)
        else:
            self.removeCase(case)
        surface.wait(0.1)

    def hasCase(self,new_case):
        """Determine if the case does not already belong to the game of life."""
        for case in self.cases:
            if case==new_case: return True
        return False

    def addCase(self,case):
        """Add a case to the given position."""
        self.cases.append(case)

    def removeCase(self,case):
        """Remove the case."""
        for i in range(len(self.cases)):
            if self.cases[i]==case:
                del self.cases[i]
                break

    def update(self):
        """Updates the game of life."""
        if not self.on: return
        positions=self.getAllPositions()
        cases=[]
        for case in positions:
            alive=(case in self.cases)
            n=self.countNeighbours(case)
            if n==2 and alive:
                cases.append(case)
            if n==3:
                cases.append(case)
        self.cases=cases

    def getAllPositions(self):
        """Return all the cases of the game and their neighbours which may be alive."""
        positions=[(x+vx,y+vy) for (x,y) in self.cases for (vx,vy) in self.getVectors()]
        return list(set(positions))


    def getVectors(self):
        """Return the basic vectors."""
        return [(x,y) for x in [-1,0,1] for y in [-1,0,1]]

    def countNeighbours(self,case):
        """Count the neibours of a case."""
        return sum([int(self.hasCase((case[0]+i,case[1]+j))) for i in [-1,0,1] for j in [-1,0,1] if (i,j)!=(0,0)])



if __name__=="__main__":
    from mycontext import Surface
    surface=Surface(name="Game of Life",fullscreen=True)
    game=GameOfLife()
    game(surface)
