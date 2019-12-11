def decorator(num_of_repeats=1):
    def actual_decorator(func):
        def wrapper(*args):
            import time
            s_time = time.time()
            result = []
            for i in range(num_of_repeats):
                result.append(func(*args))
            t_exec = round(time.time() - s_time, 4)
            print(f'{func.__name__} execution time = {t_exec} sec')
            return result
        return wrapper
    return actual_decorator


@decorator(num_of_repeats=20)
def random_generator(range_start, range_end):
    import random
    return random.randint(range_start, range_end)


result = random_generator(0, 100)
print(result)