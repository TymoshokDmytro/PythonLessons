from lesson07.practice.DBManager import DBManager


def showResult(result):
    for res in result:
        print(res)


sql_select = 'select * from products'
sql_insert = 'insert into products (title, price, categorie_id) VALUES (?, ?, ?)'

with DBManager('../classwork/shop.sqlite', False) as db:
    insert_values = [
        ('1', 1.0, None),
        ('2', 2.0, None),
        ('3', 3.0, None),
        ('4', 4.0, None),

    ]
    # db.execute_many(sql_insert, insert_values)

    result = db.execute(sql_select).fetchall()
    showResult(result)
