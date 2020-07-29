from myabstract import Segment,Point,Vector
from mycontext import Surface
import mycolors

p1=Point(-1,-1)
p2=Point(1,1)
p3=Point(0,1)

s1=Segment(p1,p2,width=3)
s2=Segment(p2,p3,width=3)

e=10e-10

surface=Surface(name="Segment Demonstration")

while surface.open:
    surface.check()
    surface.control()
    surface.clear()
    surface.show()

    p=Point(list(surface.point()))
    #if p in surface:
    s1.p2=p
    if s1.crossSegment(s2):
        s1.color=mycolors.RED
        s2.color=mycolors.RED
    else:
        s1.color=mycolors.WHITE
        s2.color=mycolors.WHITE
    l1=s1.getLine()
    l2=s2.getLine()
    l1.color=mycolors.GREEN
    l1.width=1
    l2.color=mycolors.GREEN
    l2.width=1
    l1.show(surface)
    l2.show(surface)
    s1.show(surface)
    s2.show(surface)
    p1=s1.center
    p1.show(surface,color=mycolors.RED)
    p.showText(surface,"p")
    p1.showText(surface,"p1")
    p2.showText(surface,"p2")
    p3.showText(surface,"p3")
    pl=l1.crossLine(l2)

    if pl:
        pl.show(surface,color=mycolors.RED,mode="cross",width=3)
        pl.showText(surface,"pl")
        print("in s1:",pl in s1)
        print("in s2:",pl in s2)

        v1=Vector.createFromTwoPoints(s1.p1,pl)
        v1.color=mycolors.BLUE
        v2=s1.getVector()
        v2.color=mycolors.YELLOW

        print(abs(v1.angle-v2.angle)<e)
        print(v1.norm<=v2.norm)
        print(v1.norm,v2.norm)


        v2.show(surface,s1.p1)
        v2.showText(surface,s1.p1,text="v2")
        v1.show(surface,s1.p1)
        v1.showText(surface,s1.p1,text="v1")


        v1=Vector.createFromTwoPoints(s2.p1,pl)
        v1.color=mycolors.BLUE
        v2=s2.getVector()
        v2.color=mycolors.YELLOW

        print(abs(v1.angle-v2.angle)<e)
        print(v1.angle,v2.angle)
        print(v1.norm<=v2.norm)
        print(v1.norm,v2.norm)

        v2.show(surface,s2.p1)
        v2.showText(surface,s2.p1,text="v2")
        v1.show(surface,s2.p1)
        v1.showText(surface,s2.p1,text="v1")




    surface.flip()
