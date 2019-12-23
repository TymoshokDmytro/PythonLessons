class Array:

    def __init__(self, size):
        self._array = [0] * size
        self._size = size

    def _check_range(self, index):
        if index < 0 or index > self._size:
            raise IndexError

    def __getitem__(self, index):
        self._check_range(index)
        return self._array[index]

    def __setitem__(self, index, value):
        self._check_range(index)
        self._array[index] = value

    @property
    def head(self):
        return self[0]

    @property
    def tail(self):
        return self[self._size - 1]

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._array)


a = Array(20)
print(a)
a[0] = 1
a[19] = 1


print(a.head, a.tail)

print(a)


