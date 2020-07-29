from myabstract import Form,Vector
from mycontext import Context

context=Context()

f=Form.random()
v=Vector.random()

while context:
    context.check()
    context.control()
    context.clear()

    v*=1.01
    #f.move(v)

    f.show(context)

    context.flip()
