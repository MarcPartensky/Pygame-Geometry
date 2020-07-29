# Proof of concept.

from collections import deque
import pygame as pg
from .manager import AbstractManager
from .abstract import Point, Segment, Form
from .widgets import Slider
from . import colors

import pickle


class AbstractRoomManager(AbstractManager):
    def __init__(self, points=[], **kwargs):
        super().__init__(**kwargs)
        self.points = points
        self.focus = None
        self.selection = []
        self.focus_radius = 0.5
        self.dragging = False
        self.button = None
        self.buffer = []
        self.actions = deque()
        self.widgets = []  # [Slider.createFromTuples((0, 0), (0, 10))]
        self.path = "AbstractRoom/Objects/"


    def reactKeyDown(self, key):
        super().reactKeyDown(key)
        if self.focus:
            if key == pg.K_BACKSPACE:
                self.remove()
            elif key == pg.K_SPACE:
                if self.focus in self.selection:
                    self.selection.remove(self.focus)
                else:
                    self.selection.append(self.focus)
            elif key == pg.K_a:
                f = Form(self.selection)
                self.group.append(f)
                self.selection = []
            elif key == pg.K_s:
                data = pickle.dumps([self.group, self.points])
                pickle.dump(data, open(self.path, "wb"))
            elif key == pg.K_l:
                data = pickle.load(open(self.path, "rb"))
                group, points = pickle.loads(data)
                self.points.extend(points)
                self.group.extend(group)

    def remove(self):
        for element in self.group:
            if self.focus in element.points:
                self.group.remove(element)
                print(self.focus)
        self.points.remove(self.focus)
        self.focus = None

    def reactMouseButtonUp(self, button, position):
        position = self.context.getFromScreen(position)
        self.selectUp(button, position)

    def selectUp(self, button, position):
        if button == 3:
            focus = self.focusing(Point(*position))
            if focus is None:
                focus = Point(*position)
                self.points.append(Point(*position, radius=5, conversion=False))
            if self.focus:
                if self.focus != focus:  # We don't want to create segments whose extremities are the same points
                    self.group.append(Segment(self.focus, focus))
                    self.context.console("new segment:", self.group[-1])
        self.dragging = False
        self.buffer = []

    def reactMouseButtonDown(self, button, position):
        position = self.context.getFromScreen(position)
        self.selectDown(button, position)

    def selectDown(self, button, position):
        self.focus = self.focusing(Point(*position))
        self.dragging = True
        self.button = button
        self.context.console("focus:", self.focus, self.button)

    def reactMouseMotion(self, position):
        if self.dragging and self.focus:
            position = self.context.getFromScreen(position)
            cursor = Point(*position, radius=5, conversion=False)
            focus = self.focusing(cursor)
            if self.button == 1:
                if focus:
                    cursor = focus
                self.focus.set(cursor)
            elif self.button == 3:
                if focus and focus != self.focus:
                    cursor = focus
                s = Segment(cursor, self.focus, width=2)
                self.buffer = [cursor, s]

    def focusing(self, cursor):
        focus = None
        for point in self.points:
            if Point.distance(point, cursor) < self.focus_radius:
                focus = point
                break
        return focus

    def show(self):
        super().show()
        for widget in self.widgets:
            widget.show(self.context)
        for point in self.points:
            point.show(self.context)
        for element in self.buffer:
            element.show(self.context, color=colors.GREEN)
        if self.focus is not None:
            self.focus.show(self.context, color=colors.RED)
        for element in self.selection:
            element.show(self.context, color=colors.BLUE)

    # Tracking for historic of actions for undo and redo
    def appendGroup(self, element):
        self.actions.append((0, element))
        self.group.append(element)

    def removeGroup(self, element):
        self.group.remove(element)

    def appendPoints(self, point):
        self.points.append(point)

    def removePoints(self, point):
        self.points.remove(point)


if __name__ == "__main__":
    m = AbstractRoomManager()
    m()
