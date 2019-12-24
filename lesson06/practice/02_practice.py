class ModifiedDict:

    # pop, append, insert, remove, clear
    def __init__(self, **dct):
        self._dct = {**dct}

    def __getitem__(self, key):
        return self._dct[key]

    def __setitem__(self, key, value):
        self._dct[key] = value

    # TODO
    def append(self, value):
        self._array = self._array + [value, ]

    def pop(self):
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

    def __add__(self, other):
        return self._array + [other, ]

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