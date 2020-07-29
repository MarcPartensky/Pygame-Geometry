from .abstract import Form

class Triangle(Form):
    """Representation of triangle."""
    @classmethod
    def random(cls, **kwargs):
        return super().random(n=3, **kwargs)

    def __init__(self, points, **kwargs):
        if len(points)!=3:
            raise Exception("There must be 3 points in a triangle not {}".format(len(self.points)))
        super().__init__(points, **kwargs)


if __name__=="__main__":
    from .manager import AbstractManager
    t = Triangle.random()
    c = t.center
    m=AbstractManager(t, c)
    m()