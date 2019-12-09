class Vehicle:

    _type = "Vehicle"

    def __init__(self, num_of_doors, num_of_wheels, brand, vehicle_class, transmission):
        self._num_of_doors = num_of_doors
        self._num_of_wheels = num_of_wheels
        self._brand = brand
        self._vehicle_class = vehicle_class
        self._transmission = transmission

    def get_num_of_doors(self):
        return self._num_of_doors

    def get_num_of_wheels(self):
        return self._num_of_wheels

    def get_brand(self):
        return self._brand

    def get_type(self):
        return self._type

    def get_vehicle_class(self):
        return self._vehicle_class

    def get_transmission(self):
        return self._transmission

    def set_num_of_doors(self, num_of_doors):
        self._num_of_doors = num_of_doors

    def set_num_of_wheels(self, num_of_wheels):
        self._num_of_wheels = num_of_wheels

    def set_brand(self, brand):
        self._brand = brand

    def set_type(self, type):
        self._type = type

    def set_vehicle_class(self, vehicle_class):
        self._vehicle_class = vehicle_class

    def set_transmission(self, transmission):
        self._transmission = transmission

    def move(self):
        print('Moving')

    def horn(self):
        print('Standart vehicle horn')

    def __str__(self):
        return 'type=' + self._type + \
               "\n num_of_doors=" + str(self._num_of_doors) + \
               "\n num_of_wheels=" + str(self._num_of_wheels) + \
               "\n brand=" + self._brand + \
               "\n transmission=" + self._transmission


class Car(Vehicle):

    _type = 'Light Car'

    def horn(self):
        print('Light car horn')


class Truck(Vehicle):

    _type = 'Heavy cargo truck'

    def horn(self):
        print('Heavy and loud truck horn')


car = Car(4, 4, "Toyota", "Hatchback", "auto")
truck = Truck(4, 2, 'MAN', 'cargo', 'manual')

print(car)
car.horn()

print(truck)
truck.horn()

