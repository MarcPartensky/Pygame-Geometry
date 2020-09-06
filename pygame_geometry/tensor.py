#!/usr/bin/env python
class Tensor(list):
    """Python representation of a tensor."""
    def __str__(self):
        """String representation of a tensor."""
        return f"Tensor[{','.join(map(str, self))}]"

    def __iadd__(self, tensor):
        """Add a tensor to itself."""
        for i in range(len(self)):
            self[i] += tensor[i]
        return self

    def __isub__(self, tensor):
        """Substract a tensor to itself."""
        for i in range(len(self)):
            self[i] -= tensor[i]
        return self

        



t1 = Tensor([Tensor([1,3]),1, 2])
t2 = Tensor([Tensor([1,3]),1, 2])
print(t1)
t1+=t2
print(t1)