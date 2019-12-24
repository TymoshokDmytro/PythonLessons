import requests
from bs4 import BeautifulSoup

while True:
    try:

        year = int(input('Введите год: '))
        if any((year < 1970, year > 2100)): raise TypeError('Выберете адекватное значение года(1970-2100)')
        month = int(input('Введите месяц: '))
        if any((month < 1, month > 12)): raise TypeError('Выберете адекватное значение месяца (1-12)')
        day = int(input('Введите день: '))
        if any((day < 1, day > 31)): raise TypeError('Выберете адекватное значение месяца (1-31)')
        break
    except ValueError:
        print("Ввод только циферными значениями!")
        continue
    except TypeError as e:
        print(e.args[0])
        continue

datestr = '%s-%s-%s' % (year, month, day)
print(datestr)
print()

base_url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2/{datestr}'.format(
    datestr=datestr)

# На работе прокси -___-
# proxy_host = "proxy"
# proxy_port = "3128"
# proxy_auth = ":"
# proxies = {
#     "https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
#     "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
# }

print('Retrieving information...', end='')
# proxy
# page = requests.get(base_url, proxies=proxies)
# no proxy
page = requests.get(base_url)
print('DONE')


print('Received status code', page.status_code)
html = page.text

# filename = 'soup.html'
# with open(filename, 'w') as file:
#     file.write(page.text)
#
# with open(filename, 'r') as file:
#     html = file.read()

soup = BeautifulSoup(''.join(html), features="html.parser")
# print(soup.prettify())

main_loaded = soup.find('div', {'class', 'main loaded'})

# with open(filename, 'w') as file:
#     file.write(page.text)

# print(main_loaded.prettify())

dstr = main_loaded.find('p', {'class', 'day-link'}).contents[0]

dte = main_loaded.find('p', {'class', 'date'}).contents[0]

mnth = main_loaded.find('p', {'class', 'month'}).contents[0]

dtestr = '%s %s %s' % (dstr, dte, mnth)
print('Дата =', dtestr)

link = main_loaded.find('p', {'class', 'day-link'})['data-link']
print('Ссылка =', link)
min = main_loaded.find('div', {'class', 'min'}).contents[1].contents[0]
print('Минимальная температура =', min)
max = main_loaded.find('div', {'class', 'max'}).contents[1].contents[0]
print('Минимальная температура =', max)

image_alt_text = main_loaded.find('div', {'class', 'weatherIco'})['title']
print('Чувствуется =', image_alt_text)

table_details = soup.find('table', {'class', 'weatherDetails'})

description = soup.find('div', {'class', 'description'}).contents[2]
print('Описание =', description)

gray = table_details.findAll('tr', {'class', 'gray'})

t_list = gray[0].contents
t_values = [v.contents[0] for v in t_list if v != ' ']
# print('t_values=', t_values)

temp_list = table_details.find('tr', {'class', 'temperature'}).contents
temp_values = [v.contents[0] for v in temp_list if v != ' ']
# print('temp_values=', temp_values)

p_list = gray[1].contents
p_values = [v.contents[0] for v in p_list if v != ' ']
# print('p_value=', p_values)

humidity_list = table_details.findAll('tr')[6]
humidity_values = [v.contents[0] for v in humidity_list if v != ' ']
# print('humidity_values=', humidity_values)

print()
# DATA OUTPUT
headers = ['TIME', 'TEMP', 'PRESSURE', 'HUMIDITY %']
result_info = list(zip(t_values, temp_values, p_values, humidity_values))


def printList(lst):
    for l in lst:
        print(l)


def print_row(*args):
    print("|   %-15s |   %-15s |   %-15s |   %-15s|" % args)


def fill_row(char, length):
    print(char * length)


print_row(*headers)
fill_row('-', 80)
for info in result_info:
    print_row(*info)
