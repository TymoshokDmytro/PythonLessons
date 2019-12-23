class Starter:

    def __init__(self, start, end):
        self._start = start
        self._end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self._start >= self._end:
            raise StopIteration()

        self._start += 1
        return self._start

class MyIter:

    def __init__(self, start, end):
        self._starter = Starter(start, end)

    def __iter__(self):
        return self._starter.__iter__()



obj = MyIter(0, 4)
obj_iter = iter(obj)

print(next(obj_iter))
print(next(obj_iter))
print(next(obj_iter))
print(next(obj_iter))

for i in obj:
    print(i)
