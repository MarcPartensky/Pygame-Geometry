from .abstract import Form,Point
from . import colors

import random

class Pixel:
    def __init__(self,size=(1,1),color=colors.WHITE):
        """Create a pixel."""
        self.size=size
        self.color=self.getRandomColor()

    def getRandomColor(self):
        """Return a random color."""
        r=random.randint(0,255)
        g=random.randint(0,255)
        b=random.randint(0,255)
        return (r,g,b)



    def show(self,surface,position):
        """Show the pixel on screen."""
        x,y=position
        sx,sy=self.size
        p1=Point(x,y)
        p2=Point(x+sx,y)
        p3=Point(x+sx,y+sy)
        p4=Point(x,y+sy)
        points=[p1,p2,p3,p4]
        form=Form(points,fill=True,area_color=self.color,point_show=False)
        form.show(surface)


class Sprite:
    def __init__(self,size=(10,10),pixel_size=(1,1)):
        """Create a sprite made of pixels."""
        self.pixel_size=pixel_size
        self.size=size
        sx,sy=self.size
        self.pixels=[[Pixel(self.pixel_size) for x in range(sx)] for y in range(sy)]

    def show(self,surface,position):
        """Show the sprite on the surface."""
        px,py=position
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                self.pixels[y][x].show(surface,(px+x,py+y))

    def setPixel(self,pixel,position):
        """Replace the pixel of position 'position' by the pixel 'pixel'."""
        x,y=position
        self.pixels[y][x]=pixel

    def getPixel(self,position):
        """Return the pixel of position 'position'."""
        return self.pixels[y][x]


if __name__=="__main__":
    from .surface import Surface
    surface=Surface()
    sprite=Sprite()
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        sprite.show(surface,(5,1))
        surface.flip()
