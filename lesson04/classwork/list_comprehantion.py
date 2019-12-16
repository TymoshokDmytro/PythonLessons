import time

start = time.time()

a=[]
for i in range(100):
    if i % 2 == 0:
        a.append(i)

end = time.time() - start


print('end=', '%s' % end, 'sec')

start = time.time()
odds = [i for i in range(100) if i % 2 == 0]
end_c = time.time() - start

print('end_c=', '%s' % end_c, 'sec')

if end_c < end:
    print('Comprehntions are faster')

print(odds)

dict = {1: '1',
        2: '2',
        3: '3'}

dct = [(k, v) for k, v in dict.items()]
print(dct)