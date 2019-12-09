# ========== First task =============
print('========== First task =============')
# n = int(input('Enter range: '))
n = 100
lst = list(range(n))
for item in lst:
    if item % 2 == 0: print(item)


# ========== Second task =============
print('========== Second task =============')
country_dct = {
    'Albania': 'Tirana',
    'Aljir': 'Aljir',
    'Angola': 'Lyanda',
    'Andorra': 'Andorra-la-Vellia'
}

country_lst = ['Albania', 'Angola', 'Ukraine', 'Vatican']

for country in country_lst:
    if country in country_dct: print(country, ":", country_dct[country])

# ========== Third task =============
print('========== Third task =============')
for i in range(1, 101):
    if all((i % 3 == 0, i % 5 == 0)): print('FizzBuzz')
    elif i % 3 == 0: print('Fizz')
    elif i % 5 == 0: print('Buzz')
    else: print(i)

# =========== Fourth task =============
print('========== Fourth task =============')
def bank(deposit_sum, years, percent):
    result = deposit_sum
    try:
        for year in range(1, years+1):
            result += result * (percent / 100)
    except Exception as e:
        print("Got an exception: ", e)
        return None
    return round(result, 2)

res = bank(100, 10, 5)
print("Final sum = ", res)
bank(100, '10', 5)
