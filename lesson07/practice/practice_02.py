from lesson07.practice.DBManager import DBManager, ResultType
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


class StudentsManagerException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class StudentsManager:

    def __init__(self, db_path, role):
        if not os.path.exists(db_path):
            raise Exception('Students DB not found on this path: ' + db_path)
        self._db_manager = DBManager(db_path, True)
        # self._db_manager = DBManager(db_path, False)
        if type(role) is not Role:
            raise Exception('Role must be of type Role!')
        self._role = role

    def _check_admin(func):
        def wrapper(self, *args):
            if self._role is not Role.ADMIN:
                raise StudentsManagerException("This function is allowed only for ADMINS")
            return func(self, *args)

        return wrapper

    def get_db_columns(self):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_all_students, result_type=ResultType.COLUMNS)

    def get_all_students(self):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_all_students)

    def get_student_by_id(self, id):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_student_by_field.format('id'), params=(id,))

    def get_student_by_fullname(self, fullname):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_student_by_field.format('fullname'), params=(fullname,))

    def get_student_by_stud_ticket(self, stud_ticket):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_student_by_field.format('stud_ticket'), params=(stud_ticket,))

    def get_students_by_mark_gt_than(self, mark):
        with self._db_manager as db:
            return db.execute_with_result(Queries.sql_get_students_by_mark_gt_than, params=(mark,))

    @_check_admin
    def create_student(self, fullname, department, group, avg_mark, stud_ticket):
        with self._db_manager as db:
            db.execute(Queries.sql_create_student, (fullname, department, group, avg_mark, stud_ticket))

    @_check_admin
    def update_student(self, id, field, value):
        with self._db_manager as db:
            db.execute(Queries.sql_update_student.format(field), (value, id, ))

    @_check_admin
    def remove_student(self, id):
        with self._db_manager as db:
            db.execute(Queries.sql_remove_student, (id, ))



# sm = StudentsManager('students.sqlite', Role.ADMIN)
# students = sm.get_all_students()
# showResult(students)
# sm.remove_student(10)
# print()
# students = sm.get_all_students()
# showResult(students)


def get_input(promt):
    try:
        return int(input(promt))
    except ValueError:
        raise StudentsManagerException("Option must be of integer type")

print()
print('###### Welcome to the Students Manager ######')
sm = None
db_columns = None
while True:
    print()
    print("Please choose user: ")
    print("1 = User")
    print("2 = Admin")
    print("3 = Exit")
    try:
        opt = get_input("Choose option: ")
        # Authorization block
        role = None
        if opt == 1:
           role = Role.USER
        if opt == 2:
            role = Role.ADMIN
        if opt == 3:
            break
        sm = StudentsManager('students.sqlite', role)
        db_columns = sm.get_db_columns()
        while(True):
            print()
            print("Welcome ", role.name)
            print("Please choose option: ")
            print("1 - Show all students")
            print("2 - Find student by id")
            print("3 - Find student by fullname")
            print("4 - Find student by stud_ticket")
            print("5 - Show all with avg_marks >= ")
            print("6 - Create student (ADMIN ONLY)")
            print("7 - Update student (ADMIN ONLY)")
            print("8 - Remove student (ADMIN ONLY)")
            print("9 - Exit")
            try:
                opt = get_input('Choose option:')
                if opt == 1:
                    showResult(sm.get_all_students()[0])
                if opt == 2:
                    id = get_input('Enter student id: ')
                    showResult(sm.get_student_by_id(id))
                if opt == 3:
                    fullname = input('Enter student fullname: ')
                    showResult(sm.get_student_by_fullname(fullname))
                if opt == 4:
                    stud_ticket = input('Enter student id: ')
                    showResult(sm.get_student_by_stud_ticket(stud_ticket))
                if opt == 5:
                    stud_ticket = get_input('Enter student id: ')
                    showResult(sm.get_student_by_stud_ticket(stud_ticket))
                if opt == 9:
                    break
            except StudentsManagerException as e:
                print("Error: ", e.args[0])
                continue

    except StudentsManagerException as e:
        print("Error: ", e.args[0])
        continue


print('##### BYE #####')

