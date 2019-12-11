
def sum_func(*args, **kwargs):
    print(*args)
    print(args)
    print()
    print(*kwargs)
    print(kwargs)

a = [1, 2, 3, 4]
sum_func(a, name="Hello", surname="World")



