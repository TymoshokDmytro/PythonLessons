from abc import ABC, abstractmethod


class Vehicle(ABC):

    attr = 1

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def beep(self):
        print('Default beep')

    def simpleMethod(self):
        print('Just Simple Method')


class Car(Vehicle):

    def move(self):
        print('Moving')

    def beep(self):
        super().beep()


vehicle = Car()

vehicle.move()
vehicle.beep()