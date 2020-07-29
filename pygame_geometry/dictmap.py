from collections import OrderedDict

class Map(OrderedDict):

    get = OrderedDict.__getitem__
    set = OrderedDict.__setitem__

    def __str__(self):
        """Return the string representation of a map."""
        return type(self).__name__+"{"+", ".join([f"{k}:{v}" for k,v in self.items()])+"}"

    def reset(self, m):
        """Reset the map."""
        self.clear()
        for [k, v] in m.items():
            self[k] = v

    def sort(self, f=lambda e: e):
        """Sort items."""
        self.reset(self.sorted(f))

    def sortKeys(self, f):
        """Sort items by keys."""
        self.reset(self.sortedKeys(f))

    def sortValues(self, f):
        """Sort items by values."""
        self.reset(self.sortedValues(f))

    def sorted(self, f=lambda e: e):
        """Return a sorted map."""
        return Map(sorted(self.items(), key=f))

    def sortedKeys(self, f=lambda e: e[0]):
        """Return a map sorted by keys."""
        return Map(sorted(self.items(), key=f))

    def sortedValues(self, f=lambda e: e[1]):
        """Return a map sorted by values."""
        return Map(sorted(self.items(), key=f))

    def forEach(self, f):
        """Apply f then set each value."""
        for (k,v) in self.items():
            self[k]=f(v)

    def map(self, f):
        """Apply f then yield each value."""
        for e in self.values():
            yield f(e)


if __name__=="__main__":
    d = {0:2, 1:2, 3:3}
    m = Map(d)
    print(m)
    print(m.values())
    print(m.keys())
    print(len(m))
    print(m)
    m.sort()
    print(m.sortedValues())
    print(m.sortedKeys())
    print(m.get(0))
