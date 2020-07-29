from copy import deepcopy


class Group(list):
    def __init__(self, *elements):
        """Create a group using the unpacked elements."""
        super().__init__(elements)

    def __str__(self, name=None):
        """Give a str representation of the group."""
        if name is None:
            name = type(self).__name__[0]
        return name+"[" + ",".join(map(str, self)) + "]"

    def __add__(self, other):
        """Add two groups together by concatenating the entities of each group
        into a group of type their nearest common mother class."""
        t1 = type(self).__mro__
        t2 = type(other).__mro__
        i = 0
        j = 0
        while i < len(t1) and j < len(t2) and t1[i] != t2[j]:
            if i <= j:
                i += 1
            else:
                j += 1
        return t1[i](*self, *other)

    def __sub__(self, other):
        """Remove all elements of the first group that are in the second.
        Note that adding then subtracting a group to another does not give
        you the initial group."""
        group = deepcopy(self)
        for element in group:
            if element in other:
                group.remove(element)
        return group

    def __rmul__(self, n):
        """Return a duplicate of the group with n deep copies of the initial elements."""
        if not isinstance(n, int):
            raise ValueError("Groups can only be duplicated.")
        group = type(self)()
        for i in range(n):
            group.extend(deepcopy(self))
        return group

    def __call__(self, function):
        """Call a function on each element."""
        group = deepcopy(self)
        for (i, element) in enumerate(group):
            group[i] = function(element)
        return group

    def __invert__(self):
        """Return a group without any duplicate without preserving the order."""
        return type(self)(*set(list(self)))

    def __or__(self, other):
        """Return the union of both groups."""
        return ~(self+other)

    def __xor__(self, other):
        """Return the intersection of both groups."""
        g1 = self - other
        g2 = other - self
        return ~(g1+g2)

    def __and__(self, other):
        """Return the intersection of both groups."""
        group = Group()
        for element in ~(self+other):
            if element in self and element in other:
                group.append(element)
        return group

    def getElements(self):
        """Return the elements of the group.
        Note: This is an expensive operation to avoid when possible."""
        return list(self)

    def setElements(self, elements):
        """Set the elements of the group.
        Note: This is an expensive operation to avoid when possible."""
        self.clear()
        self.extend(elements)

    def delElements(self):
        """Delete all elements."""
        self.clear()

    elements = property(getElements, setElements, delElements)

    def __hash__(self):
        """Hash lazily with id."""
        return id(self)

    def appendleft(self, element):
        """Append an element to the left."""
        self.reverse()
        self.append(element)
        self.reverse()

    def flattened(self):
        """Flatten the tree."""
        tree = Group()
        for element in self:
            if isinstance(element, Group):
                tree.extend(element.flattened())
            else:
                tree.append(element)
        return tree


class Tree(Group):
    """A tree is an object specialized in groups of groups."""

    def flattened(self):
        """Flatten the tree."""
        tree = type(self)()  # We create an empty instance of the tree type
        for element in self:
            if isinstance(element, Tree):
                tree.extend(element.flattened())
            else:
                tree.append(element)
        return tree

    def flatten(self):
        """Flatten in a bad way."""
        self.elements = self.flattened()
        raise Warning("This method is not efficient, use 'flattened' when possible.")


if __name__ == "__main__":
    # Definition
    g1 = Group(1, 2, 4, 5)
    g2 = Group(1, 5, 6)

    # Operations
    gp = g1 + g2
    gn = g1 - g2

    # Deep copy of elements
    g5 = 3 * g1
    g5[1] = 0
    print(g5)

    # Copy of reference
    g3 = g2
    g2[2] = 4
    print(g3)

    # Apply a function
    f = lambda x: x ** 2
    print(g1(f))

    # Invert
    print(~g1)

    del g3.elements
    g3.elements = deepcopy(g5.elements)
    print(g3)

    # Trees
    t1 = Tree(g1, g2, 5)
    t2 = Tree(t1, ~t1)
    t3 = t2(Tree)  # Make trees of all elements
    print(t3)

    # Flatten the tree in 2 ways.
    t4 = deepcopy(t3)  # 1
    print(t3.flattened())
    # t4.flatten()  # 2
    # print(t4)

    print(len(g1.elements))




