from .surface import Surface
from .form import Form
from .point import Point

class Set:
    def __init__(self,forms):
        self.forms=forms


    def move(self):
        pass

    def control(self):
        pass

if __name__=="__main__":
    forms=[Form([Point(random.randint(-10,10),random.randint(-10,10)) for i in range(10)]) for i in range(3)]
    set=Set(forms)
    surface=Surface()
    while surface.open:
        surface.check()
        set.control()
        surface.clear()
        set.show()
        surface.flip()
