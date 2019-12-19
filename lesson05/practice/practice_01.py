from threading import Thread
from time import sleep


def thread_decorator(name, daemon):
    def actual_decorator(func):
        def wrapper(*args):
            t = Thread(target=func, args=(*args, ), name=name, daemon=daemon)
            print(f'Thread {name} started')
            t.start()

        return wrapper
    return actual_decorator


@thread_decorator('thread', False)
def func(range_num, step):
    for i in range(range_num):
        sleep(step)
        print('Sleep for', i+1)


func(5, 1)
print('MAIN FINISHED')
