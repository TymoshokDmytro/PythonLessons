class Dot:

    def __init__(self, x, y, z):
        if not all([type(x) in (int, float), type(y) in (int, float), type(z) in (int, float)]):
            raise Exception('Coordinates must be integer type')
        self._x = x
        self._y = y
        self._z = z

    def set_x(self, new_x):
        self._x = new_x

    def get_x(self):
        return self._x

    def set_y(self, new_y):
        self._y = new_y

    def get_y(self):
        return self._y

    def set_z(self, new_z):
        self._z = new_z

    def get_z(self):
        return self._z

    def __add__(self, obj1):
        return Dot(self.get_x() + obj1.get_x(),
                   self.get_y() + obj1.get_y(),
                   self.get_z() + obj1.get_z())

    def __sub__(self, obj1):
        return Dot(self.get_x() - obj1.get_x(),
                   self.get_y() - obj1.get_y(),
                   self.get_z() - obj1.get_z())

    def __mul__(self, obj1):
        return Dot(self.get_x() * obj1.get_x(),
                   self.get_y() * obj1.get_y(),
                   self.get_z() * obj1.get_z())

    def __div__(self, obj1):
        if any([obj1.get_x() == 0, obj1.get_y() == 0, obj1.get_z() == 0]):
            raise Exception('Second dot coordinates contains zero.' +
                            '\nCannot proceed operation that causes zero division error' +
                            '\n Dots: ' + str(self) + ' | ' + str(obj1))
        return Dot(self.get_x() / obj1.get_x(),
                   self.get_y() / obj1.get_y(),
                   self.get_z() / obj1.get_z())

    def __truediv__(self, other):
        return self.__div__(other)

    def __str__(self):
        return 'Dot(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ')'


dot_1 = Dot(1, 2, 3)
dot_2 = Dot(1, 2, 3)
print('Dot_1:', dot_1)
print('Dot_2:', dot_2)
print()

dot_3 = dot_1 * dot_2
print("Addition: " + str(dot_3))
dot_3 = dot_1 - dot_2
print("Subtraction: " + str(dot_3))
dot_3 = dot_1 * dot_2
print("Multiplication: " + str(dot_3))
dot_3 = dot_1 / dot_2
print("Division: " + str(dot_3))
