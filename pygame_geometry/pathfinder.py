from . import colors
import random

class PathFinder:
    def __init__(self,size=(10,10),difficulty=0.2):
        sx,sy=size
        self.colors=[colors.WHITE,colors.RED]
        self.map=[[self.colors[int(random.uniform(0,1)<difficulty)] for y in range(sy)] for x in range(sx)]
        self.paths=[[None for y in range(sy)] for x in range(sx)]
        self.start=(0,0)
        self.arrival=(sx,sy)
        stx,sty=self.start
        self.paths[stx][sty]=0


    def __call__(self,context):
        while context.open:
            self.events()
            self.update()
            self.show(context)

    def events(self):
        pass

    def update(self):
        cases=self.getPathsCases()
        neighbours=self.getCasesNeighbours(cases)

    def getPathColor(self,x,y):
        sm=max(sx,sy)
        p=self.paths[x][y]
        c=255*p/sm
        return (0,c,0)

    def showMap(self,context):
        sx,sy=self.size
        for x in range(sx):
            for y in range(sy):
                self.showCase(context,x,y,self.map[x][y])

    def showPaths(self,context):
        sx,sy=self.size
        for x in range(sx):
            for y in range(sy):
                color=self.getPathColor(x,y)
                self.showCase(context,x,y,color)

    def showCase(self,context,x,y,color):
        context.draw.rect(context.screen,color,(x,y,1,1),1)




    def show(self,context):
        context.check()
        context.control()
        context.clear()
        context.show()
        self.showMap(context)
        #self.showPaths(context)
        #self.showSolution(context)
        context.flip()

    def getSize(self):
        sx=len(self.map)
        sy=len(self.map[0])
        return (sx,sy)

    size=property(getSize)



if __name__=="__main__":
    from .surface import Context
    context=Context()
    pf=PathFinder()
    pf(context)
