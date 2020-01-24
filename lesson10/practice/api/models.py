from mongoengine import *

connect('rest_blog_db')


class Tag(Document):
    tag = StringField(max_length=16, required=True)


class Author(Document):
    fullname = StringField(max_length=64, required=True)
    posts_count = IntField(min_value=0)


class Post(Document):
    title = StringField(max_length=64, required=True)
    description = StringField(max_length=8192, required=True)
    creation_date = DateTimeField(required=True)
    author = ReferenceField(Author)
    views = IntField(min_value=0, required=True)
    tag = ListField(ReferenceField(Tag))
