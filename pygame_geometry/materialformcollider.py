from .materialform import MaterialForm
from .abstract import Point,Form,Segment,Vector

import math

class MaterialFormHandler:
    def __init__(self,material_forms):
        """Create material form collider object."""
        self.forms=material_forms
        self.time=0.1

    def update(self,t):
        """Update the forms and deal with its collisions."""
        self.updateForms(t)
        self.dealCollisions()

    def updateForms(self,t):
        """Update the forms."""
        for form in self.forms:
            form.update(t)

    def dealCollisions(self):
        """Deal with all collisions."""
        l=len(self.forms)
        for i in range(l):
            for j in range(i):
                f1=self.forms[i]
                f2=self.forms[j]
                self.collide(f1,f2)

    def rotate(self,angle=math.pi/2,point=Point(0,0)):
        """Rotate the forms using an angle and a point."""
        for form in self.forms:
            form.rotate(angle,point)


    def collide(self,object1,object2):
        """Deal with the collisions of two objects 'object1' and 'object2'."""
        #I've got no clue how to do such a thing
        #I just know that i need the motions of the forms, the coordonnates of its points and their masses.
        ap1=object1.points
        bp1=[Point.createFromVector(p1.getNextPosition(self.time)) for p1 in ap1]
        ls1=[Segment(a1.abstract,b1) for (a1,b1) in zip(ap1,bp1)]
        ap2=object2.points
        bp2=[Point.createFromVector(p2.getNextPosition(self.time)) for p2 in ap2]
        ls2=[Segment(a2.abstract,b2) for (a2,b2) in zip(ap2,bp2)]
        points=[]
        for s1 in ls1:
            for s2 in ls2:
                print(s1,s2)
                point=s1.crossSegment(s2)
                if point:
                    print(point)
                    points.append(point)
        return points

    def show(self,surface):
        """Show the material forms on the surface."""
        for form in self.forms:
            form.show(surface)

    def affectFriction(self):
        """Affect all entities with frixion for all dimensions."""
        for entity in self.entities:
            for i in range(len(entity.center.position)):
                entity.velocity=[self.factor*entity.velocity[0],self.factor*entity.velocity[1]]

    def affectCollisions(self):
        """Affect all entities with collisions between themselves."""
        l=len(self.entities)
        for y in range(l):
            for x in range(y):
                self.affectCollision(self.entities[y],self.entities[x])

    def affectCollision(self,entity1,entity2):
        x1,y1=entity1.position
        x2,y2=entity2.position
        r1=entity1.radius
        r2=entity2.radius
        if sqrt((x1-x2)**2+(y1-y2)**2)<r1+r2:
            self.affectVelocity(entity1,entity2)


    def affectVelocity(self,entity1,entity2):
        x1,y1=entity1.position
        x2,y2=entity2.position
        vx1,vy1=entity1.velocity
        vx2,vy2=entity2.velocity
        m1=entity1.mass
        m2=entity2.mass
        if x2!=x1:
            angle=-atan((y2-y1)/(x2-x1))
            ux1,uy1=self.rotate2(entity1.velocity,angle)
            ux2,uy2=self.rotate2(entity2.velocity,angle)
            v1=[self.affectOneVelocity(ux1,ux2,m1,m2),uy1]
            v2=[self.affectOneVelocity(ux2,ux1,m1,m2),uy2]
            entity1.velocity=self.rotate2(v1,-angle)
            entity2.velocity=self.rotate2(v2,-angle)

    def affectOneVelocity(self,v1,v2,m1,m2):
        return (m1-m2)/(m1+m2)*v1+(2*m2)/(m1+m2)*v2

    def rotate2(self,velocity,angle):
        vx,vy=velocity
        nvx=vx*cos(angle)-vy*sin(angle)
        nvy=vx*sin(angle)+vy*cos(angle)
        return [nvx,nvy]

if __name__=="__main__":
    from .surface import Surface
    surface=Surface(name="Material Form Handler")
    ps1=[Point(0,0),Point(0,1),Point(1,1),Point(1,0)]
    f1=Form(ps1)
    f1=MaterialForm.createFromForm(f1)
    f1.velocity=Vector(1,1)
    ps2=[Point(0,0),Point(0,2),Point(2,2),Point(2,0)]
    f2=Form(ps2)
    f2=MaterialForm.createFromForm(f2)
    forms=[f1,f2]
    handler=MaterialFormHandler(forms)

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        handler.update(1)
        handler.rotate(0.1)
        handler.show(surface)
        surface.flip()
