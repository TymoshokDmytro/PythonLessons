
class Singleton:

    _objects = None

    def __new__(cls, *args, **kwargs):
        if cls._objects:
            # raise Exception('Object already created')
            return cls._objects

        cls._objects = super().__new__(cls, *args, **kwargs)
        return cls._objects


obj1 = Singleton()
obj2 = Singleton()
print(obj1)
print(obj2)

