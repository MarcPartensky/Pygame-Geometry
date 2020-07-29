# Description

This is a framework based on pygame that allows an easier process for making games. This is so much more than a tool kit.
Tested in pygame2 not in pygame1.

# Installation

```bash
pip install pygame-geometry
```

# Quick examples:

# Draw some moving Points and a Circle
```python
from pygame_geometry.abstract import Point, Circle
from pygame_geometry.context import Context
from pygame_geometry import colors

context = Context(name="title") # create a context similar to a pygame surface

p1 = Point(2,2)
p2 = Point(3,2, color=colors.BLUE)
c = Circle(0, -1, radius=2, color=colors.RED)

# main game loop
while context.open:
    # clear the window
    context.clear()
    # check quit event (empty pygame event buffer by doing so)
    context.check()
    # move and zoom around the scene
    context.control()

    # update objects
    p1.rotate(0.01, p2)
    c.x += 0.01

    # show objects
    p1.show(context)
    p2.show(context)
    c.show(context)

    # flip the screen
    context.flip()
```

[![Watch the video](https://media.giphy.com/media/KfN5xs8RPlYfOf9h2W/giphy.gif)](https://www.youtube.com/watch?v=2PInBSgEUq8)


# Draw Bezier Curves
```python
from pygame_geometry.context import Surface
from pygame_geometry.curves import Trajectory, BezierCurve
from pygame_geometry.abstract import Point
from pygame_geometry import colors

import random

# create objects
surface=Surface(name="Curves demonstration")
l=10
points=[Point(2*x,random.randint(-5,5)) for x in range(l)]
t=Trajectory(points,segment_color=colors.GREEN)
b=BezierCurve(points,segment_color=colors.RED)
n=0
ncp=50 #number construction points

while surface.open:
    # surface stuff
    surface.check()
    surface.clear()
    surface.control()
    surface.show() # show a math grid in background

    # update
    Point.turnPoints([1/1000 for i in range(l)],points)
    n=(n+1)%(ncp+1)
    b.showConstruction(surface,n/ncp)
    p1=b(n/ncp)
    p2=Point(*t(n/ncp))

    # show
    t.show(surface)
    b.show(surface)
    p1.show(surface,color=colors.YELLOW,radius=0.1,fill=True)
    p2.show(surface,color=colors.YELLOW,radius=0.1,fill=True)

    # flip
    surface.flip()
```

[![Watch the video](https://media.giphy.com/media/L1F6advUQQUaAF1zj4/giphy.gif)](https://www.youtube.com/watch?v=ffTXqMtSfTk)

# Controls

* Space: Switch to next mode.
* Enter: Go back to the center.
* Up/Down/Right/Left Arrow: Move arround.
* Right/Left Shift: Zoom in or out.
* Quit/Escape: Quit.

# Geometry objects

Geometry components added:
* point
* segment
* vector
* line
* halfline

But also:
* circle
* rectangle
* square
* polygon
* triangle
* bezier curve
* trajectory

# Physics/Maths objects

* force
* motion
* body
* polynomial
* perlin noise


# Game objects

* entity
* anatomy
* widget
* menu
* manager

# More technical physics objects

* material
* material form
* material circle
* material formcollider

# Enjoy!