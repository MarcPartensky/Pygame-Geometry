from .abstract import Circle,Point,Vector
from .motion import Motion
from . import colors

import random

class MaterialCircle:
    def random(corners=[-1,-1,1,1],radius=random.uniform(0,1),color=colors.WHITE):
        """Create a random material circle."""
        p=Vector.random()
        v=Vector.random()
        a=Vector.random()
        m=Motion([p,v,a])
        return MaterialCircle(m,radius,color)

    def __init__(self,motion=Motion,radius,color):
        """Create a material circle using position, radius and color."""
        self.motion=motion
        self.radius=radius
        self.color=color

    def show(self,surface,color=None):
        """Show the material circle on the surface and an optional color."""
        if not color: color=color
        c=self.getAbstractCircle()
        c.show(surface,color=color)

    def showMotion(self,surface,color=None):
        """Show the motion of the material circle using the surface and an optional color."""
        if not color: color=color
        self.motion.show(surface,color)

    def onCollision(self,point):
        """React to a physical collision between two objects using the material point of collision."""
        vector=Vector.createFromPoint(point)
        a=vector.angle()
        v1=self.motion.getVelocity()
        v2=point.motion.getVelocity()
        v1.rotate()



        pm=point.mass
        px,py=point.position

    def affectVelocity(self,entity1,entity2):
        x1,y1=entity1.position
        x2,y2=entity2.position
        vx1,vy1=entity1.velocity
        vx2,vy2=entity2.velocity
        m1=entity1.mass
        m2=entity2.mass
        if x2!=x1:
            angle=-atan((y2-y1)/(x2-x1)) #Will trigger an error if both object are on a vertical line
            ux1,uy1=self.rotate(entity1.velocity,angle)
            ux2,uy2=self.rotate(entity2.velocity,angle)
            v1=[self.affectOneVelocity(ux1,ux2,m1,m2),uy1]
            v2=[self.affectOneVelocity(ux2,ux1,m1,m2),uy2]
            entity1.velocity=self.rotate(v1,-angle)
            entity2.velocity=self.rotate(v2,-angle)

    def affectOneVelocity(self,v1,v2,m1,m2):
        return (m1-m2)/(m1+m2)*v1+(2*m2)/(m1+m2)*v2

    def rotate(self,velocity,angle):
        vx,vy=velocity
        nvx=vx*cos(angle)-vy*sin(angle)
        nvy=vx*sin(angle)+vy*cos(angle)
        return [nvx,nvy]





if __name__=="__main__":
    from .surface import Surface
    surface=Surface()
    mc=MaterialCircle()
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        mc.show(surface)
        surface.flip()
