import sqlite3

conn = sqlite3.connect('shop.sqlite')
conn
cursor = conn.cursor()
result = cursor.execute('select * from products')

print(result)

cursor.close()
conn.close()