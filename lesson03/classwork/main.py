import threading


def a(a_arg):
    print(a_arg)

    def b(b_arg):
        print(b_arg)

    return b


#Decorators basics
def get_exec_time(func):
    def wrapper(*args):
        import time
        s_time = time.time()
        result = func(*args)
        t_exec = round(time.time() - s_time, 4)
        print(f'execution time = {t_exec} sec')
        return result
    return wrapper


# result = decorator(random_generator, )(0, 100)
@get_exec_time
def random_generator(range_start, range_end):
    import random
    return random.randint(range_start, range_end)

random_generator(0, 100)