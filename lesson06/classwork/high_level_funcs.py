list_of_names = ['john', 'helen', 'nencie', 'jack']


def printList(lst):
    print()
    for l in lst:
        print(l)


def making_upper(string):
    return string.upper()


# 1
results = []
for name in list_of_names:
    results.append(making_upper(name))

printList(results)

# 2
results_2 = [making_upper(name) for name in list_of_names]
printList(results_2)

# 3
results_3 = map(making_upper, list_of_names)
print()
print(results_3)
print(list(results_3))

# 4
results_4 = map(lambda x: x.upper(), list_of_names)
print()
print(results_4)
print(list(results_4))

# 5
results_5 = map(lambda x, y: (x.upper(), y.upper()), list_of_names, list_of_names)
print()
print(results_5)
print(list(results_5))


def func(extra_value, **kwargs):
    for k, v in kwargs:
        if v == extra_value:
            del kwargs[k]
            kwargs.pop(k)
    return kwargs

extra_value = 'token'
kwargs = {
    'sum': 12,
    'id': 134,
    'comment': "user_comment",
    'token': 'uuid_token'
}
fiter = filter(lambda k, v: k != extra_value, kwargs.items())

print(dict(fiter))