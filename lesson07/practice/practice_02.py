from lesson07.practice.DBManager import DBManager, ResultType
from lesson07.practice.queries import Queries
from enum import Enum, unique

import os


@unique
class Role(Enum):
    USER = 1,
    ADMIN = 2


def print_row(*args, offset=15):
    print(("|   %-" + str(offset) + "s") * (len(args)) % args)


def fill_row(char, length):
    print(char * length)


def showResult(result):
    print()
    print_row(*db_columns)
    fill_row('-', 110)
    for res in result:
        print_row(*res)


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
    def create_student(self, fullname, department, group, str_marks, stud_ticket):
        with self._db_manager as db:
            marks_eval = eval(str_marks)
            db.execute(Queries.sql_create_student, (fullname, department, group, stud_ticket))
            id = db.execute_with_result(Queries.sql_get_max_student_id, result_type=ResultType.FETCH_ONE)[0]
            marks = [(id, v) for v in marks_eval]
            db.execute_many(Queries.sql_insert_mark, marks)

    @_check_admin
    def update_student(self, id, field, value):
        with self._db_manager as db:
            db.execute(Queries.sql_update_student.format(field), (value, id,))

    @_check_admin
    def rewrite_marks(self, id, str_marks):
        with self._db_manager as db:
            marks = [(id, v) for v in eval(str_marks)]
            db.execute(Queries.sql_remove_marks_by_id, (id,))
            db.execute_many(Queries.sql_insert_mark, marks)

    @_check_admin
    def remove_student(self, id):
        with self._db_manager as db:
            db.execute(Queries.sql_remove_student, (id,))
            db.execute(Queries.sql_remove_marks_by_id, (id,))


def get_input(promt, v_type='int'):
    try:
        if v_type == 'float':
            return float(input(promt))
        return int(input(promt))
    except ValueError:
        raise StudentsManagerException("Option must be of {} type".format(v_type))


def raise_not_admin_func():
    raise StudentsManagerException('This function is only for ADMINS')


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
        while (True):
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
            print("8 - Rewrite marks by id (ADMIN ONLY)")
            print("9 - Remove student (ADMIN ONLY)")
            print("10 - Exit")
            try:
                opt = get_input('Choose option: ')
                if opt == 1:
                    showResult(sm.get_all_students())
                if opt == 2:
                    id = get_input('Enter student id: ')
                    showResult(sm.get_student_by_id(id))
                if opt == 3:
                    fullname = input('Enter student fullname: ')
                    showResult(sm.get_student_by_fullname(fullname))
                if opt == 4:
                    stud_ticket = input('Enter student ticket num: ')
                    showResult(sm.get_student_by_stud_ticket(stud_ticket))
                if opt == 5:
                    mark = get_input('Enter the mark to see the students with higher marks: ', 'float')
                    showResult(sm.get_students_by_mark_gt_than(mark))
                if opt == 6:
                    if role is not Role.ADMIN:
                        raise_not_admin_func()
                    print("Enter values for new student")
                    fullname = input('Enter fullname: ')
                    department = input('Enter department: ')
                    group = input('Enter group: ')
                    avg_mark = input('Enter marks as string with comas(3.0, 4.15, 5.0): ')
                    stud_ticket = input('Enter stud_ticket: ')
                    sm.create_student(fullname, department, group, avg_mark, stud_ticket)
                    print('Student', fullname, 'created.')
                if opt == 7:
                    if role is not Role.ADMIN:
                        raise_not_admin_func()
                    id = get_input("Enter student id to update: ")
                    student = sm.get_student_by_id(id)
                    if not student:
                        raise StudentsManagerException('No student with such id')
                    print("Available columns to update: ")
                    for i, column in enumerate(db_columns):
                        if i == 0: continue
                        print(i, '-', column)
                    field_num = get_input("Enter field number to update: ")
                    if field_num > len(db_columns) or field_num == 0:
                        raise StudentsManagerException('No such option in columns - ', field_num)
                    field = db_columns[field_num]
                    if field == 'avg_mark':
                        value = get_input('New value for field "{}": '.format(field), 'float')
                    else:
                        value = input('New value for field "{}": '.format(field))
                    sm.update_student(id, field, value)
                    print("Student with id =", id, 'successfully updated')
                if opt == 8:
                    if role is not Role.ADMIN:
                        raise_not_admin_func()
                    id = get_input("Enter student id to rewrite_marks: ")
                    str_marks = input('Enter marks as string with comas(3.0, 4.15, 5.0): ')
                    sm.rewrite_marks(id, str_marks)
                if opt == 9:
                    if role is not Role.ADMIN:
                        raise_not_admin_func()
                    id = get_input("Enter student id to remove: ")
                    sm.remove_student(id)
                if opt == 10:
                    break
            except StudentsManagerException as e:
                print("Error: ", e.args[0])
                continue

    except StudentsManagerException as e:
        print("Error: ", e.args[0])
        continue

print('##### BYE #####')
