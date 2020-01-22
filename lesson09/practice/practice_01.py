import json

from mongoengine import *

from lesson09.practice.practice_02 import *


class Mark(Document):
    value = IntField(min_value=1, max_value=5, required=True, unique=True)

    def __str__(self):
        return f'{self.value}'


class Kurator(Document):
    fullname = StringField(max_length=64, required=True)

    def __str__(self):
        return f'Kurator[fullname={self.fullname}]'


# ФИО, группа, оценки, куратор, студента, факультет
class Student(Document):
    fullname = StringField(max_length=64, required=True)
    group = StringField(max_length=16, required=True)
    department = StringField(max_length=32, required=True)
    marks = ListField(ReferenceField(Mark))
    kurator = ReferenceField(Kurator)

    def get_keys(self):
        return json.loads(self.to_json()).keys()

    def __str__(self):
        return f'Student[fillname={self.fullname}, group={self.group}, department={self.department}, marks={self.marks}, kurator={self.kurator}]'


def get_random_kurator():
    return random.choice(Kurator.objects.filter())


def get_random_marks(size=10):
    return [random.choice(Mark.objects.filter()) for i in range(size)]


class Department:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Department, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_students_size():
        return len(Student.objects.filter())

    @staticmethod
    def get_student(**kwargs):
        return Student.objects.filter(**kwargs)

    @staticmethod
    def create_student(**kwargs):
        Student(**kwargs).save()

    @staticmethod
    def delete_student(**kwargs):
        Student.delete(**kwargs)

    @staticmethod
    def update_student(**kwargs):
        Student.update(**kwargs)


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
    dep = Department()
    print(dep.get_student(kurator=Kurator.objects.first()))
    # save students to departament
