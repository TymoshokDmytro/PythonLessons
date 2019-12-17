from abc import ABC, abstractmethod
from datetime import date


class Person(ABC):

    def __init__(self, name, bday):
        if not type(bday) == date:
            raise TypeError('Birthday value must be of datetime type')
        self._name = name
        self._bday = bday

        now = date.today()
        age = now.year - self._bday.year
        month = now.month - self._bday.month
        day = now.day - self._bday.day
        if any((month < 0, day <= 0)):
            age += 1

        self._age = age

    def get_age(self):
        return self._age

    @abstractmethod
    def get_info(self):
        pass


class Student(Person):

    def __init__(self, name, bday, department, course):
        super().__init__(name, bday)
        self._department = department
        self._course = course

    def get_info(self):
        return f'Student[name={self._name}, ' \
               f'bday={self._bday.strftime("%b %d %Y")}, ' \
               f'department={self._department}, ' \
               f'course={self._course}]' \
               f'age={self._age}'


# Абитуриент
class Enrollee(Person):

    def __init__(self, name, bday, department):
        super().__init__(name, bday)
        self._department = department

    def get_info(self):
        return f'Enrollee[name={self._name}, ' \
               f'bday={self._bday.strftime("%b %d %Y")}, ' \
               f'department={self._department}]' \
               f'age={self._age}'


class Teacher(Person):

    def __init__(self, name, bday, job, workyears):
        super().__init__(name, bday)
        self._job = job
        self._workyears = workyears

    def get_info(self):
        return f'Teacher[name={self._name}, ' \
               f'bday={self._bday.strftime("%b %d %Y")}, ' \
               f'job={self._job}, ' \
               f'workyears={self._workyears}, ' \
               f'age={self._age}'


t = Teacher('Teacher1', date(1967, 12, 15), 'PhD Philosopy', 3)

e = Enrollee('Enrollee1', date(2002, 12, 15), 'Electromechanics')

s = Student('Student1', date(1998, 4, 12), 'Polithology', 4)

lst = [t, e, s]


def getPersonsWithAgeOf(persons, age):
    return [p for p in persons if p.get_age() >= age]


def printPersonsInfo(persons):
    for person in persons:
        print(person.get_info())


printPersonsInfo(lst)
print()
# Enrollee wont be printed
print('Print everyone who are > 18')
printPersonsInfo(getPersonsWithAgeOf(lst, 18))