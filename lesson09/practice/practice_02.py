import random
import string

from lesson09.practice.practice_01 import Student, Mark, Kurator
from utils.utils import generate_string


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
        Student.drop_collection()
        for i in range(size):
            Student(fullname=generate_string(20, 10),
                    group=generate_string(10, 5, (string.ascii_uppercase + string.digits)),
                    department=generate_string(15, 10),
                    marks=[random.choice(self._marks_objects) for i in range(marks_size)],
                    kurator=random.choice(self._kurators)).save()

        return Student.objects.filter()

    @staticmethod
    def drop_students():
        Student.drop_collection()

    @staticmethod
    def get_all_students():
        return Student.objects.filter()

    @staticmethod
    def get_all_students_count():
        return Student.objects.count()