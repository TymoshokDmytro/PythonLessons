class UpperCaseMetaClass(type):

    def __new__(cls, name, base, attrs):
        for i in range(5):
            attrs.update({'var_' + str(i): i})
        return super().__new__(cls, name, base, attrs)


class Inherited():
    pass


class MyClass(Inherited, metaclass=UpperCaseMetaClass):

    _attributes_of_class = 'Attr'

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f'MyClass[x={self._x}, y={self._y}]'

print(dir(MyClass))

