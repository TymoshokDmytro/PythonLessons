
class ComplexNumber():

    def __init__(self, real, img):
        self._real = real
        self._img = img

    def __str__(self):
        return 'ComplexNumber{' + self._real + ' + ' + self._img + 'i}'

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
            self.get_real() + other.get_real(),
            self.get_img() + other.get_img()
        )

    def __sub__(self, other):
        return ComplexNumber(
            self.get_real() - other.get_real(),
            self.get_img() - other.get_img()
        )

#TODO
    def __mul__(self, other):
        return ComplexNumber(
            (self.get_real() * other.get_real()) - (self.get_img() * other.get_img()),
            (self.get_real() * other.get_real()) - (self.get_img() * other.get_img())
        )