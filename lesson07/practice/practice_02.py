from lesson07.practice.DBManager import DBManager
from lesson07.practice.queries import Queries
from enum import Enum, unique

import os


@unique
class Role(Enum):
    USER = 1,
    ADMIN = 2


def showResult(result):
    for res in result:
        print(res)


class StudentManagerException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class StudentsManager:

    def __init__(self, db_path, role):
        if not os.path.exists(db_path):
            raise Exception('Students DB not found on this path: ' + db_path)
        self._db_manager = DBManager(db_path, True)
        if type(role) is not Role:
            raise Exception('Role must be of type Role!')
        self._role = role

    def _check_admin(func):
        def wrapper(self, *args):
            if self._role is not Role.ADMIN:
                raise StudentManagerException("This function is allowed only for ADMINS")
            return func(self, *args)

        return wrapper

    def get_all_students(self):
        with self._db_manager as db:
            return db.execute(Queries.sql_get_all_students).fetchall()

    def get_student_by_fullname(self, fullname):
        with self._db_manager as db:
            return db.execute(Queries.sql_get_student_by_field.format('fullname'), (fullname,)).fetchall()

    def get_student_by_ticket_num(self, stud_ticket):
        with self._db_manager as db:
            return db.execute(Queries.sql_get_student_by_field.format('stud_ticket'), (stud_ticket,)).fetchall()


sm = StudentsManager('students.sqlite', Role.USER)
students = sm.get_student_by_ticket_num('FI00001')
showResult(students)
