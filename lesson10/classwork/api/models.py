import datetime

from mongoengine import *

connect('developers_db')


class Project(Document):
    title = StringField(max_length=128)
    description = StringField(max_length=8192)
    deadline = DateField(required=True)


class Developer(Document):
    POSITIONS = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('DBA', 'DBA'),
    )

    fullname = StringField(min_length=3, required=True)
    position = StringField(min_length=0, choises=POSITIONS)
    project = ReferenceField(Project)


if __name__ == '__main__':
    positions = ('Backend', 'Frontend', 'DBA')

    # dev1 = Developer.objects.create(fullname='Developer_1', position=positions[0])
    # dev2 = Developer.objects.create(fullname='Developer_2', position=positions[1])

    # project = Project.objects.create(
    #     title='Facebook',
    #     description='Social Network',
    #     deadline=datetime.datetime.now()
    # )
    #
    # dev1 = Developer.objects.create(fullname='Developer_1',
    #                                 position=positions[0],
    #                                 project=project)
