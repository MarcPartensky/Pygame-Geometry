from .abstract import Point, Segment, Form, Vector
from . import colors

import random
import math


class Graph:
    """Representation of a discrete graph with its points and connections."""

    @classmethod
    def random(cls, n=10):
        """Create a random graph. By default the points are placed on the unit
        circle."""
        points = []
        d = 2 * math.pi
        r = 1
        for i in range(n):
            a = d * i / n
            x = r * math.cos(a)
            y = r * math.sin(a)
            points.append(Point(x, y))
        connections = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0:
                    connections.append((i, j))
        return cls(points, connections)

    def __init__(self, points, connections, point_color=colors.RED,
            segment_color=colors.BLUE, vector_color=colors.GREEN):
        """Create a graph from its points and their connections."""
        # Maths
        self.points = points
        self.connections = connections
        # Colors
        self.point_color = point_color
        self.segment_color = segment_color
        self.vector_color = vector_color

    def show(self, context):
        """Show all the points and their connections."""
        self.showSegments(context)
        #self.showVectors(context)
        self.showPoints(context)

    def showPoints(self, context):
        """Show all the points of the graph on the context."""
        for point in self.points:
            point.show(context, self.point_color, fill=True)

    def showSegments(self, context):
        """Show all the segments of the graph."""
        for segment in self.segments:
            segment.show(context)

    def showVectors(self, context):
        """Show the vectors."""
        for (i, vector) in enumerate(self.vectors):
            vector.show(context, self.points[self.connections[i][0]])

    def getSegments(self):
        """Return the segments that connect the points with their connections."""
        return [Segment(self.points[c[0]], self.points[c[1]],\
                    color=self.segment_color) for c in self.connections]

    def getVectors(self):
        """Return the vectors that connect the points with their connections.
        Unlike the segments the vectors show the orientation."""
        return [Vector.createFromTwoPoints(self.points[c[0]], self.points[c[1]],\
                    color=self.vector_color) for c in self.connections]

    segments = property(getSegments)
    vectors = property(getVectors)


if __name__ == "__main__":
    from .context import Context
    context = Context()
    g = Graph.random()

    while context:
        context.check()
        context.control()
        context.clear()
        context.show()

        g.show(context)

        context.flip()
