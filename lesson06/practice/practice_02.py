class ModifiedDict:

    # pop, append, insert, remove, clear
    def __init__(self, dct):
        self._dct = dct

    def __getitem__(self, key):
        return self._dct[key]

    def __setitem__(self, key, value):
        self._dct[key] = value

    def get(self, key):
        return self._dct[key]

    def items(self):
        return [(key, self._dct[key]) for key in list(self._dct)]

    def keys(self):
        return list(self._dct)

    def values(self):
        return [self._dct[key] for key in list(self._dct)]

    # TODO
    def __add__(self, other):
        temp_dct = self._dct.copy()
        for key in other.keys():
            temp_dct[key] = other[key]
        return temp_dct

    def __str__(self):
        return str(self._dct)


dct = ModifiedDict({'1': 1})
print(dct)

a = dct.get('1')
print(a)

items = dct.items()
print(items)

dct['2'] = 2
print(dct)

keys = dct.keys()
print(keys)

values = dct.values()
print(values)

new_dct = dct + {'3': 3}
print(new_dct)
print(dct)

