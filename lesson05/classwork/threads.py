from threading import Thread
import time


def get_exec_time(start_time):
    return round(time.time() - start_time, 2)


def testing_threads():
    print('Thread executed')
    time.sleep(3)
    print('Thread finished')

# start_time = time.time()
# for i in range(20):
#     testing_threads()
#
# print(get_exec_time(start_time))

#parallel
# thread_list = []
# start_time = time.time()
# for i in range(20):
#     t = Thread(target=testing_threads())
#     thread_list.append(t)
# print(get_exec_time(start_time))

#join


t = Thread(target=testing_threads(), daemon=True)
t.start()
t.join()
print('MAIN THREAD FINISHED')

