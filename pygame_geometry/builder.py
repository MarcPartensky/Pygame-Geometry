"""This program is deprecated."""

from .abstract import Point, Form, Vector
from .body import Body
from pygame.locals import *
from . import colors

import pygame
import copy


class Builder:
    """Allow the user to create, manipulate and destroy body objects."""
    def __init__(self, context):
        """Create a builder from scratch."""
        self.bodies = []
        self.context = context
        self.focus_index = None
        # self.time=time.time()

    def __call__(self):
        """Main loop of the builder."""
        self.show()
        while self.context.open:
            self.events()
            self.update()
            self.show()

    def events(self):
        """Deal with the user input."""
        cursor = copy.deepcopy(Point(*self.context.point()))
        click = self.context.click()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.context.open = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.context.open = False

            if event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.focus_index = None
                    for body in self.bodies:
                        if cursor in body.absolute:
                            self.focus_index = self.bodies.index(body)
                    if self.focus_index:
                        self.bodies[self.focus_index].position = Vector(*cursor)

                if event.button == 3:
                    c = copy.deepcopy(cursor)
                    if self.focus_index == None:
                        self.focus_index = len(self.bodies)
                        f = Form([c])
                        self.bodies.append(Body.createFromForm(f))
                    else:
                        fa = copy.deepcopy(self.bodies[self.focus_index].absolute)
                        fa.points.append(c)
                        self.bodies[self.focus_index].absolute = fa

            if event.type == MOUSEMOTION:
                if self.focus and click:
                    self.focus.position = Vector(*cursor)

        keys = pygame.key.get_pressed()

        if keys[K_DOWN]:
            self.context.draw.plane.position[1] -= 1
        if keys[K_UP]:
            self.context.draw.plane.position[1] += 1
        if keys[K_LEFT]:
            self.context.draw.plane.position[0] -= 1
        if keys[K_RIGHT]:
            self.context.draw.plane.position[0] += 1

        if keys[K_LSHIFT]:
            self.context.draw.plane.zoom([0.9, 0.9])
        if keys[K_RSHIFT]:
            self.context.draw.plane.zoom([1.1, 1.1])

    def update(self):
        """Update the builder by incrementing the time and updating the objects."""
        self.updateBodies()

    def updateBodies(self):
        """Update the bodies of the builder."""
        for body in self.bodies:
            body.update()

    def show(self):
        """Show the builder by showing the context and its components on the screen."""
        self.context.clear()
        self.context.show()
        self.showBodies()
        if self.focus:
            self.showFocus()
        self.showInfo()
        self.context.flip()

    def showBodies(self):
        """Show the bodies on the context."""
        for body in self.bodies:
            body.absolute.showPoints(self.context)

    def showFocus(self):
        """Show the focus in color."""
        fc = copy.deepcopy(self.focus)
        fc.form.side_color = colors.RED
        fc.position.show(self.context)
        fc.show(self.context)

    def showInfo(self):
        """Show informations in the absolute screen."""
        x = 10
        y = 10
        self.context.draw.window.print("focus: " + str(bool(self.focus)), (x, y))
        y += 30
        self.context.draw.window.print("focus_index: " + str(self.focus_index), (x, y))
        y += 30
        for i in range(len(self.bodies)):
            self.context.draw.window.print("body: " + str(self.bodies[i]), (x, y))
            y += 30

    def getFocus(self):
        """Return the body being focused."""
        if self.focus_index is not None:
            return self.bodies[self.focus_index]
        else:
            return None

    def setFocus(self, body):
        """Set the focus using a body."""
        if body is not None:
            if not (body in self.bodies):
                self.bodies.append(body)
            self.focus_index = self.bodies.index(body)
        else:
            self.focus_index = None

    focus = property(getFocus, setFocus)


if __name__ == "__main__":
    from context import Context

    context = Context(fullscreen=True)
    builder = Builder(context)
    builder()
