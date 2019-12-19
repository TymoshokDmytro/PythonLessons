
class ComplexNumber():

    def __init__(self, real, img):
        self._real = real
        self._img = img

    def __str__(self):
        return f'ComplexNumber({self._real} + {self._img}i)'

    def get_real(self):
        return self._real

    def set_real(self, real):
        self._real = real

    def get_img(self):
        return self._img

    def set_img(self, img):
        self._img = img

    def __add__(self, other):
        return ComplexNumber(
            self._real + other.get_real(),
            self._img + other.get_img()
        )

    def __sub__(self, other):
        return ComplexNumber(
            self._real - other.get_real(),
            self._img - other.get_img()
        )

    def __mul__(self, other):
        return ComplexNumber(
            (self._real * other.get_real()) - (self._img * other.get_img()),
            (self._img * other.get_real()) + (self._real * other.get_img())
        )

    def __truediv__(self, other):
        a = self._real
        b = self._img
        c = other.get_real()
        d = other.get_img()

        if any((c == 0, d == 0)):
            raise ZeroDivisionError('Division by zero found: ' +
                                    '\n ' + str(self) +
                                    '\n ' + str(other))

        real = ((a * c) + (b * d)) / ((c ** 2) + (d ** 2))
        img = ((b * c) - (a * d)) / ((c ** 2) + (d ** 2))

        return ComplexNumber(round(real, 4), round(img, 4))


cmplx1 = ComplexNumber(3, 1)
cmplx2 = ComplexNumber(5, -2)
print(f'cmplx1={cmplx1}')
print(f'cmplx2={cmplx2}')

cmplx_res = cmplx1 + cmplx2
print(f'Addition: {cmplx_res}')

cmplx_res = cmplx1 - cmplx2
print(f'Subtraction: {cmplx_res}')

cmplx_res = cmplx1 * cmplx2
print(f'Multiplication: {cmplx_res}')

cmplx_res = cmplx1 / cmplx2
print(f'Division: {cmplx_res}')
