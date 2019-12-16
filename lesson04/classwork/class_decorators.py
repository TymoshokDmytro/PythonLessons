class Shop:

    _total_sales = 0

    def __init__(self, name, sales):
        self._name = name
        self._sales = sales
        Shop._total_sales += sales

    @classmethod
    def get_total_sales(cls):
        return cls._total_sales

    @staticmethod
    def get_total_static_sales():
        return Shop._total_sales

    def __call__(self, *args, **kwargs):
        print(f'Hi, i am object of {self.__class__.__name__}')


print(f'total={Shop.get_total_sales()}')

shop_obj = Shop('ATB', 4000)
shop_obj()

class Decorator:

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print(f'Decorating {self._func.__name__}')
        self._func(args)


@Decorator
def func(x):
    print(f'x={x}')

func(9)
