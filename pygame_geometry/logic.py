from .case import Case
from .abstract import Circle
from . import colors


class Operator(Case):
    def __init__(self, *args, **kwargs):
        """Create an operator using case arguments such as position and size."""
        super().__init__(*args, **kwargs)

    def showBox(self, surface):
        """Show the box on the given surface."""


class Adder(Operator):
    def __init__(self, *args, **kwargs):
        """Create an adder using case arguments such as position and size."""
        super().__init__(*args, **kwargs)
        self.inputs = 3
        self.outputs = 2

    def __call__(self, a, b, c):
        """Perform the adder operation using binary arguments a,b and c and returning the sum and the carry."""
        pass  # Might be made using circuit class


class LogicGate(Case):
    def __init__(self, position, size=(1, 1), color=colors.WHITE, fill=False):
        """Create a logic gate using case arguments such as position and size."""
        super().__init__(position, size, color, fill)
        self.name = "Logic Gate"
        self.inputs = 2
        self.outputs = 1

    def __str__(self):
        """Return the string representation of the and gate."""
        return self.name

    __repr__ = __str__

    def showCase(self, *args, **kwargs):
        """Show the form on screen."""
        self.showForm(*args, **kwargs)

    def showText(self, context, text=None):
        """Show the text on the surface."""
        if not text:
            text = self.name
        point = self.center()
        point.showText(context, text)

    def show(self, context, **kwargs):
        """Show the and gate."""
        self.showText(context)
        self.showCase(context, **kwargs)

    def showCircle(self, context, **kwargs):
        """Show a circle at the back of the logic gate when necessary."""
        pass


class AndGate(LogicGate):
    def __init__(self, *args, **kwargs):
        """Create an and gate using logic gate arguments."""
        super().__init__(*args, **kwargs)
        self.name = "&"

    def __call__(self, a, b):
        """Perform the and gate known operation using a and b in binary."""
        return a and b


class OrGate(LogicGate):
    def __init__(self, *args, **kwargs):
        """Create an or gate."""
        super().__init__(*args, **kwargs)
        self.name = ">=1"

    def __call__(self, a, b):
        """Perform the or gate known operation using a and b in binary."""
        return a or b


class XorGate(LogicGate):
    def __init__(self, *args, **kwargs):
        """Create an or gate."""
        super().__init__(*args, **kwargs)
        self.name = "=1"

    def __call__(self, a, b):
        """Perform the or gate known operation using a and b in binary."""
        return (a or b) and (a != b)


class NorGate(LogicGate):
    def __init__(self, *args, **kwargs):
        """Create an or gate."""
        super().__init__(*args, **kwargs)
        self.name = "<=1"

    def __call__(self, a, b):
        """Perform the or gate known operation using a and b in binary."""
        return (a or b) and (a != b)


class Not(LogicGate):
    def __init__(self, *args, **kwargs):
        """Create an or gate."""
        super().__init__(*args, **kwargs)
        self.name = "1"

    def __call__(self, a):
        """Perform the or gate known operation using a and b in binary."""
        return not a


class Button(Circle):
    def __init__(self, default_value=0, colors=[colors.BLACK, colors.RED]):
        """Create a pushable button."""
        self.default_value = default_value
        self.colors = colors

    def push(self):
        """Allow the user to push the button."""


class Circuit:
    def __init__(self, logic_gates=[]):
        """Create a circuit object."""
        self.logic_gates = logic_gates
        self.connexions = []

    def show(self, surface):
        """Show the circuit by showing all its logic gates."""
        for gate in self.logic_gates:
            gate.show(surface)


if __name__ == "__main__":
    from .context import Context

    context = Context(name="Logic Gates")
    g1 = OrGate([1, 1])
    g2 = AndGate([2, 1])
    gs = [g1, g2]
    c = Circuit(gs)

    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        c.show(context)
        context.flip()
