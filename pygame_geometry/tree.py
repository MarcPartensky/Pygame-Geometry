from .dictmap import Map


class Tree(Map):
    """
    Ideas for new method names:
    deploy, diffuse, broadcast, transmit, disseminate
    """
    def __init__(self, *args, disperse=True):
        super().__init__(*args)
        if disperse:
            self.disperse()

    # def __str__(self,n=1):
        # return "".join(map(lambda e:str(dict(e[1])) if isinstance(e, Tree) else str(e), self.items()))
        # self.deploy()
        # if n==1:
        #     return super().__str__()
        # else:
        #     return str(dict(self))

    def subMap(self,f):
        """Apply f and yield each sub value."""
        for e in self.subValues():
            yield f(e)

    def getLevel(self, n=1):
        """Return the level in the Tree."""
        m = n
        for e in self.values():
            if isinstance(e, Tree):
                l = e.getLevel(n+1)
                if l>m: m = l
        return m

    def search(self, key):
        """Search for an element using its key in the Tree."""
        try:
            return self.get(key)
        except:
            for e in self.values():
                if isinstance(e,Tree):
                    v = e.search(key)
                    if v: return v
            # raise IndexError(f"{key} not found")

    def find(self, path):
        """Find an element using its path in the Tree."""
        if len(path)==1:
            return self[path[0]]
        else:
            return self[path[0]].find(path[1:])

    def put(self, path, value):
        """Set an element in the Tree."""
        if len(path)==1:
            self[path[0]] = value
        else:
            if path[0] in self:
                self[path[0]].set(path[1:], value)
            else:
                self[path[0]] = Tree()
                self[path[0]].put(path[1:], value)

    def distribute(self,f):
        """Distribute f for all values."""
        for (k,v) in self.items():
            self[k] = f(v)

    def spread(self, f):
        """Apply f to set all sub values."""
        for (k,v) in self.items():
            if isinstance(v,Tree):
                v.spread(f)
            else:
                self[k] = f(v)

    def deploy(self, f):
        """Apply f over all sub values to return a new Tree."""
        m = self.copy()
        m.spread(f)
        return m

    def propagate(self, f):
        """Propagate f over all full values."""
        for (k,v) in self.items():
            self[k] = f(v)
            if isinstance(v,Tree):
                self[k].propagate(f)

    def disperse(self):
        """Disperse the Tree type."""
        for (k,v) in self.items():
            try: #Check if v is iterable
                iter(v)
                self[k] = Tree(v)
                self[k].disperse()
            except:
                pass

    def subKeys(self):
        """Iterate all sub keys."""
        for (k,v) in self.items():
            if isinstance(v,Tree):
                for k in v.subKeys():
                    yield k
            else:
                yield k

    def fullKeys(self):
        """Iterate all full keys."""
        for (k,v) in self.items():
            yield k
            if isinstance(v,Tree):
                for k in v.fullKeys():
                    yield k

    def subValues(self):
        """Iterate all sub values."""
        for (k,v) in self.items():
            if isinstance(v,Tree):
                for v in v.subValues():
                    yield v
            else:
                yield v

    def fullValues(self):
        """Iterate all full values."""
        for (k,v) in self.items():
            yield v
            if isinstance(v,Tree):
                for v in v.fullValues():
                    yield v

    def subPaths(self):
        """Iterate all sub paths."""
        for (k,v) in self.items():
            if isinstance(v,Tree):
                for p in v.subPaths():
                    yield [k]+p
            else:
                yield [k]

    def fullPaths(self):
        """Iterate all full paths."""
        for (k,v) in self.items():
            yield [k]
            if isinstance(v,Tree):
                for p in v.fullPaths():
                    yield [k]+p

    def map(self, f):
        return []

    level = property(getLevel)


if __name__ == "__main__":
    c = {2:{2:3},1:3}
    d = {1: 5, 3: 4, 0: 3}
    a = {6 : d, 3:{6:d}}
    b = {7:d, 9:{2:a, 8:d}, 0:{5:2}}
    print(list(sorted(d)))

    t = Tree({11:[1,2],6:{9:b}, 8:8})
    t.put(["osef",9,1,2], 5)
    t.put([0,5],8)
    print('searching:', t.search(3))
    print("finding:", t.find([6,9,9,2,6,3]))
    print(t)
    print(t.getLevel())
    print(t.level)
    d = {
        "SuperGroup":{
            "PlayerGroup":{
                "Player0":"player0",
                "Player1":"player1"
            },
            "AsteroidGroup":{
                "Asteroid1":"asteroid1",
                "Asteroid2":"asteroid2"
            },
            "Test": [1,2,3]
        }
    }
    g = Tree(d)
    print(g.search("Player0"))
    print(g.search("Asteroid1"))

    print(list(g.subKeys()))
    print(list(g.fullKeys()))
    print(list(g.subValues()))
    print(list(g.fullValues()))
    print(list(g.subPaths()))
    print(list(g.fullPaths()))

    for i,v in enumerate(t.subValues()):
        if i==0:
            print(v)
            v[0] = 5
            print("i==3:",v)
    print(t)

    print(c)
    for i, v in enumerate(c.values()):
        print(v)
        # if i==0:
        #     print(v)
        #     v[2] = 12879439
        #     print("i=3:", v)

    print(c)

    print(list(g.subValues()))

    l = g.search("Test")
    l[0] = 9
    # print(g.search("bla"))
    # print(t.get(3))
