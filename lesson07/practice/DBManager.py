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
