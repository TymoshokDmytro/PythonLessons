class Cat:
    def __init__(self, name):
        self._name = name

    def meow(self):
        print('Meow!')

    def say_my_name(self):
        print(f'My name: {self._name}')

    def __add__(self, obj2):
        return Cat(self._name + obj2._name)


cat1 = Cat('cat1')
cat2 = Cat('cat2')

cat3 = cat1 + cat2
cat3.say_my_name()


# Function as object
# def second_func():
#     print('second_func')
#
#
# def my_func(func):
#     func()
#     pass
# my_func(second_func)


def square_root(number):
    return number ** 2


def printIterable(iterable):
    for iter in iterable:
        print(iter)


sq_root = lambda number: number ** 2
print(sq_root(10))
map_value = map(sq_root, range(100))
printIterable(map_value)


