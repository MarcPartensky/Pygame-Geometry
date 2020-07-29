from .abstract import Form, Point, Segment
import numpy as np
import colors
import random


class ComplexForm(Form):
    """A complex form is basically a form made of multiple subforms."""

    @classmethod
    def random(cls, nf=3, np=5, nfp=3, **kwargs):
        """Create a random complex form."""
        points=Form.random(n=np).points
        l=len(points)
        forms=[]
        for j in range(nf):
            f=Form([],area_color=colors.random(),fill=True)
            d=[]
            for i in range(nfp):
                d.append(random.randint(0,l-1))
            forms.append((d,f))
        return cls(points, forms, **kwargs)

    def __init__(self, points, forms=[], **kwargs):
        """Create a complex form."""
        super().__init__(points, **kwargs)
        self._forms = forms

    @property
    def forms(self):
        """Read the forms."""
        forms=[]
        for j in range(len(self._forms)):
            form=self._forms[j][1]
            for i in self._forms[j][0]:
                form+=self.points[i]
            forms.append(form)
        return forms

    def show(self, context):
        """Show the complex form on the surface."""
        super().show(context)
        self.showForms(context)

    def showForms(self,context):
        """Show the subforms of the complex form."""
        for form in self.forms:
            form.show(context)




if __name__ == "__main__":
    from .manager import Manager

    class Tester(Manager):
        def __init__(self):
            super().__init__()
            self.c=ComplexForm.random()
            print(self.c.forms[0])

        def update(self):
            self.c.rotate(0.1)

        def show(self):
            self.c.show(self.context)

    t=Tester()
    t()
