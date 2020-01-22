from mongoengine import *


class Project(Document):
    description = StringField(max_length=8192)
    deadline = DateField(required=True)


class Developer(Document):
    POSITIONS = (
        ('1', 'Backend'),
        ('2', 'Frontend'),
        ('1', 'DBA'),
    )

    fullname = StringField(min_length=3, required=True)
    position = StringField(min_length=3, choises=POSITIONS)
    project = ReferenceField(Project)
