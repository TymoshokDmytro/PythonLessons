import json
import random
import string

from mongoengine import *
from utils.utils import generate_string, generate_random_int


class Mark(Document):
    value = IntField(min_value=1, max_value=5, required=True, unique=True)

    def __str__(self):
        return f'{self.value}'


class Kurator(Document):
    fullname = StringField(max_length=64, required=True)

    def __str__(self):
        return f'Kurator[fillname={self.fullname}]'


# ФИО, группа, оценки, куратор, студента, факультет
class Student(Document):
    fullname = StringField(max_length=64, required=True)
    group = StringField(max_length=16, required=True)
    department = StringField(max_length=32, required=True)
    marks = ListField(ReferenceField(Mark))
    kurator = ListField(ReferenceField(Kurator))

    def get_keys(self):
        return json.loads(self.to_json()).keys()

    def __str__(self):
        return f'Student[fillname={self.fullname}, group={self.group}, department={self.department}, marks={self.marks}, kurator={self.kurator}]'


class StudentMongoGenerator:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StudentMongoGenerator, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if Kurator.objects.count() == 0:
            for i in range(10):
                Kurator.objects.create(fullname=generate_string(15, 10))
        self._kurators = Kurator.objects.filter()

        if Mark.objects.count() == 0:
            for i in range(1, 6):
                Mark(value=i).save()
        self._marks_objects = Mark.objects.filter()

    def generate_students(self, size, marks_size=10):
        students = []
        for i in range(size):
            students.append(Student(fullname=generate_string(20, 10),
                                    group=generate_string(10, 5, (string.ascii_uppercase + string.digits)),
                                    department=generate_string(15, 10),
                                    marks=[random.choice(self._marks_objects) for i in range(marks_size)],
                                    kurator=[random.choice(self._kurators)]).save())

        return students

    @staticmethod
    def drop_students():
        Student.drop_collection()

    @staticmethod
    def get_all_students():
        return Student.objects.filter()

    @staticmethod
    def get_all_students_count():
        return Student.objects.count()


class Department:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Department, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_students_size():
        return len(Student.objects.filter())

    @staticmethod
    def get_random_marks(size=10):
        return [random.choice(Mark.objects.filter()) for i in range(size)]

    @staticmethod
    def get_random_kurator():
        return random.choice(Kurator.objects.filter())

    @staticmethod
    def create_student(fullname, group, department, marks, kurator):
        Student(fullname=fullname,
                group=group,
                department=department,
                marks=marks,
                kurator=[kurator]).save()


    #TODO from here
    @staticmethod
    def delete_student(self, field_name, value):
        pass


if __name__ == '__main__':
    connect('faculty_db')
    smg = StudentMongoGenerator()
    # DROP STUDENTS collection
    # smg.drop_students()

    # GENERATE NEW STUDENTS
    # generated_students = smg.generate_students(50)
    # print(generated_students)

    # GET ALL STUDENTS
    students = smg.get_all_students()
    dep = Department(students)
    print(dep.get_students_size())
    # save students to departament
