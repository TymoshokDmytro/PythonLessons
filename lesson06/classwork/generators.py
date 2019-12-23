def counter(start, end):
    while start <= end:
        yield start
        start += 1


c = counter(0, 3)
it = iter(c)

print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))
