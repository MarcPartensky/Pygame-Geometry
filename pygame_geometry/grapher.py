# graph, curve, plot
import numpy as np
import math
import itertools
import random

from . import colors
from .manager import SimpleManager


class Function:
    """Function that can be studied with maths."""

    def __init__(self, function, name=None):
        """Create a Function object using a default function."""
        self.function = function
        if name == None:
            self.name = str(self.function)

    def __str__(self):
        return name

    def getDefinition(self):
        """Return the domain of definition of the function."""
        pass  # I have no idea how to proceed

    def getLimits(self):
        """Return the limits of the function."""
        pass


class Graph(Function):
    """Graph that can be shown on a surface."""

    def __init__(self, function, name=None, color=colors.WHITE):
        """Create a graph using a function."""
        super().__init__(function, name)
        self.color = color


class Grapher(SimpleManager):
    def __init__(self, context, functions):
        """Create an object that can display graphs."""
        self.functions = functions
        self.context = context
        self.sample_number = 200
        self.setColors()
        self.setNames()

    def setColors(self):
        """Set the colors of the functions."""
        self.colors = [colors.RED, colors.BLUE, colors.GREEN, colors.YELLOW, colors.PURPLE, colors.ORANGE,
                       colors.BROWN]
        self.colors += [colors.random() for i in range(len(self.functions) - len(self.colors))][:len(self.functions)]

    def setNames(self):
        """Set the names of the function in the context's console."""
        self.context.text = []
        for i in range(len(self.functions)):
            self.context.text.append(str(self.functions[i]))

    def getInterval(self):
        """Return xmin and xmax."""
        cs = self.context.corners
        return (cs[0], cs[2])

    def sampleFunctions(self, functions):
        """Sample all the functions one by one."""
        ymin = self.context.ymin
        ymax = self.context.ymax
        return [self.sampleFunction(function, ymin, ymax) for function in functions]

    def sampleFunction(self, function, ymin, ymax):
        """Return n points of the graph."""
        xmin, xmax = self.getInterval()
        n = self.sample_number
        xl = np.linspace(xmin, xmax, n)
        return [(x, function(x)) for x in xl if ymin < function(x) < ymax]

    def cleverlySampleFunction(self, function):
        """Sample a function in an optimized way to get the nicest visualisation possible with the less points as possible."""
        pass

    def update(self):
        """Update the samples."""
        self.graphs = self.sampleFunctions(self.functions)

    def show(self):
        """Show the graphs."""
        self.context.clear()
        self.context.control()
        self.context.show()
        self.showGraphs(self.graphs)
        # Its just for a demo, it will be removed later
        if "points" in self.__dict__:
            self.showPoints()
        self.context.showConsole()
        self.context.flip()

    def showPoints(self):
        """Show the points on the context."""
        for point in self.points:
            point.show(self.context)

    def showGraphs(self, graphs):
        """Show the graphs on the screen."""
        for (i, graph) in enumerate(graphs):
            color = self.colors[i]
            print(color)
            self.showGraph(graph, color)

    def showGraph(self, graph, color=colors.WHITE):
        """Show a graph on the screen."""
        self.context.draw.lines(self.context.screen, color, graph, connected=False)


if __name__ == "__main__":
    from .context import Context
    from .polynomial import Polynomial
    from .abstract import Point

    context = Context(name="Grapher Demonstration")
    xs, ys = [1, 2, -4, -6, 4], [1, -3, -2, 5, -2]
    ps = [Point(x, y, radius=2, conversion=False) for (x, y) in zip(xs, ys)]
    p = Polynomial.createFromInterpolation(xs, ys)
    fs = [math.sin, math.cos, math.tan, p]
    grapher = Grapher(context, fs)
    grapher.points = ps
    grapher()
