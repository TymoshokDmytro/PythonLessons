# Class definition
class Vehicle:

    # __slots__ = ['num_of_doors', 'num_of_wheels', 'brand']

    vehicle_type = 'Car'

    def __init__(self, num_of_doors, num_of_wheels, brand):
        self.num_of_doors = num_of_doors
        self.num_of_wheels = num_of_wheels
        self.brand = brand

    def move(self):
        print('Moving')

    def __str__(self):
        return 'vehicle_type=' + self.vehicle_type + \
               "\n num_of_doors=" + str(self.num_of_doors) + \
               "\n num_of_wheels=" + str(self.num_of_wheels) + \
               "\n brand=" + self.brand


vehicle = Vehicle(4, 4, "AuchanCar")
vehicle.num_of_wheels = 10
print(vehicle.num_of_doors)
print(vehicle.num_of_wheels)
print(vehicle.brand)
print(vehicle)

print(Vehicle.vehicle_type)
vehicle.vehicle_type = 'Truck'
print(vehicle.vehicle_type)

class Car(Vehicle):

    def __init__(self, num_of_doors, num_of_wheels, brand, max_weight):
        super().__init__(num_of_doors, num_of_wheels, brand)
        self._engine = 'V-8'
        self.max_weight = max_weight

    def transport_smth(self, weight, thing):
        print(f'Transporting {thing}. Max weight is {weight}')

    def _change_oil(self):
        print('Changing oil')

    # def get_engine(self):
    #     return self._engine
    #
    # def set_engine(self, new_engine):
    #     self._engine = new_engine

car = Car(4, 4, "SomeCar", 400)
car.transport_smth(200, 'Animals')
car.move()
print(car._engine)

print(dir(car))

print(car.__class__.__dict__)





