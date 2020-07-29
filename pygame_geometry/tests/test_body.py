from myabstract import Form,Point
from mybody import Body
from mycontext import Context

import copy
import mycolors

ps=[Point(10,2),Point(12,5),Point(15,-2)]
f=Form(ps)
b=Body.createFromAbsolute(f)

context=Context()
while context.open:
    context.check()
    context.control()
    context.clear()
    context.show()

    p=Point(*context.point())

    nb=copy.deepcopy(b)
    nba=copy.deepcopy(nb.absolute)
    nba.points.append(p)
    for point in nba.points:
        point.show(context,color=mycolors.BLUE)
    nb.absolute=nba

    nb.show(context)
    nb.absolute.center.show(context,color=mycolors.RED)

    context.flip()
