import sqlite3


class DBManager:

    def __init__(self, conn_str, autocommit=False):
        self.conn_str = conn_str
        self._autocommit = autocommit

    def __enter__(self):
        self._conn = sqlite3.connect(self.conn_str)
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def autocommit(func):
        def wrapper(self, *args):
            res = func(self, *args)
            if self._autocommit is True:
                self._conn.commit()
            return res

        return wrapper

    @autocommit
    def execute(self, sql, params=None):
        if params is None:
            return self._cursor.execute(sql)
        else:
            return self._cursor.execute(sql, params)

    @autocommit
    def execute_many(self, sql, params):
        return self._cursor.executemany(sql, params)


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