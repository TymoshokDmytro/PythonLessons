class ArrayList:

    # pop, append, insert, remove, clear
    def __init__(self, *lst):
        self._array = [*lst]
        self._size = len(lst)

    def _check_range(self, index):
        if index < 0 or index > self._size:
            raise IndexError

    def __getitem__(self, index):
        self._check_range(index)
        return self._array[index]

    def __setitem__(self, index, value):
        self._check_range(index)
        self._array[index] = value

    def append(self, value):
        self._size += 1
        self._array = self._array + [value, ]

    def pop(self):
        if self._size == 0:
            raise IndexError('No item to pop in list')
        result = self._array[self._size - 1]
        del self._array[self._size - 1]
        self._size -= 1
        return result

    def insert(self, index, value):
        self._check_range(index)
        self._array = self._array[:index] + [value, ] + self._array[index:]
        self._size += 1

    def remove(self, index):
        self._check_range(index)
        del self._array[index]
        self._size -= 1

    def clear(self):
        self._array = []
        self._size = 0

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


a = ArrayList(9, 10, 11)

a.append(12)
a.append(13)
a.append(14)
print(a)
a.insert(3, 23)
print(a)
a.remove(1)
print(a)
a.clear()
print(a)
