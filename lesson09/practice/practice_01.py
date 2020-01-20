import json
from mongoengine import *

from utils.utils import showResult


class Mark(Document):
    value = IntField(min_value=1, max_value=5, required=True)


class Kurator(Document):
    fullname = StringField(max_length=64, required=True)


# ФИО, группа, оценки, куратор, студента, факультет
class Student(Document):
    fullname = StringField(max_length=64, required=True)
    group = StringField(max_length=16, required=True)
    department = StringField(max_length=32, required=True)
    marks = ListField(ReferenceField(Mark))
    kurator = ListField(ReferenceField(Kurator))

    def get_keys(self):
        return json.loads(self.to_json()).keys()


class Department(Document):
    students = ListField(ReferenceField(Student))

    # def __str__(self):
    #     for student in self.students:
    #         showResult((student.fullname,))


if __name__ == '__main__':
    connect('faculty_db')

    # Kurator.objects.create(fullname='Kurator_1')
    # Kurator.objects.create(fullname='Kurator_2')
    # Kurator.objects.create(fullname='Kurator_3')

    kurator_1 = Kurator.objects.get(fullname='Kurator_1')
    kurator_2 = Kurator.objects.get(fullname='Kurator_2')
    kurator_3 = Kurator.objects.get(fullname='Kurator_3')


    Student.objects.create()