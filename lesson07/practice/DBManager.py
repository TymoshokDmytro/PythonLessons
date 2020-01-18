import sqlite3
from enum import Enum, unique

@unique
class ResultType(Enum):
    COLUMNS = 1
    FETCH_ALL=2
    FETCH_ONE=3
    RESULT_AND_COLUMNS = 4
    AS_DICT_LIST_WITH_COLUMNS_KEYS = 5
    CURSOR = 6

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
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if self._autocommit is True:
                self._conn.commit()
            return res

        return wrapper

    @autocommit
    def execute_with_result(self, sql, params=None, result_type=None):
        result = self.execute(sql, params)

        if result_type == ResultType.CURSOR:
            return result
        if result_type == ResultType.COLUMNS:
            return [col[0] for col in result.description]
        if result_type == ResultType.FETCH_ONE:
            return result.fetchone()
        if result_type == ResultType.RESULT_AND_COLUMNS:
            return result.fetchall(), [col[0] for col in result.description]
        if result_type == ResultType.AS_DICT_LIST_WITH_COLUMNS_KEYS:
            columns = [col[0] for col in result.description]
            data = result.fetchall()
            return [dict(zip(columns, value)) for value in data]
        else:
            return result.fetchall()

    @autocommit
    def execute(self, sql, params=None):
        if params is None:
            return self._cursor.execute(sql)
        else:
            return self._cursor.execute(sql, params)

    @autocommit
    def execute_many(self, sql, params):
        return self._cursor.executemany(sql, params)
