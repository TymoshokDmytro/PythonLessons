# with open('file.txt', 'r') as file:
#     for line in file.readlines():
#         print(line.replace('\n', ''))

class MyContextManager:

    def __init__(self, number):
        self._number = number

    def __enter__(self):
        print('Context manager openned')
        return self._number

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_val)
        self._number = 0


a = MyContextManager(10)
with a as number:
    print(number)

print(a._number)
