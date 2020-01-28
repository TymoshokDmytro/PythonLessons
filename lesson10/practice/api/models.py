import datetime
import random

from mongoengine import *
import lorem
from faker import Faker

connect('rest_blog_db')


class Tag(Document):
    tag = StringField(max_length=16, required=True)

    def __str__(self):
        return f'Tag[tag={self.tag}]'


class Author(Document):
    fullname = StringField(max_length=64, required=True)
    posts_count = IntField(min_value=0)

    def __str__(self):
        return f'Author[fullname={self.fullname}, posts_count={self.posts_count}]'


class Post(Document):
    title = StringField(max_length=64, required=True)
    description = StringField(max_length=8192, required=True)
    creation_date = DateTimeField(default=datetime.datetime.now())
    author = ReferenceField(Author)
    views = IntField(min_value=0, default=0)
    tags = ListField(ReferenceField(Tag))

    def __str__(self):
        return f'Post[title={self.title}, ' \
               f'description={self.description}, ' \
               f'creation_date={self.creation_date}, ' \
               f'author={self.author},' \
               f'views={self.views},' \
               f'tags={self.tags}]'


class BlogDataGenerator:

    @staticmethod
    def generate_blog_data(author_num=10, tag_num=20, posts_num=100):
        Post.drop_collection()
        Author.drop_collection()
        Tag.drop_collection()

        for i in range(tag_num):
            Tag.objects.create(tag='#' + lorem.sentence().split(' ')[0][:16])

        for i in range(author_num):
            Author.objects.create(fullname=(lorem.sentence().split(' ')[0] + ' '
                                            + lorem.sentence().split(' ')[1] + ' '
                                            + lorem.sentence().split(' ')[2])[:64], posts_count=0)

        for i in range(posts_num):
            Post.objects.create(title=lorem.sentence().split(' ')[0][:64],
                                description=lorem.sentence()[:8192],
                                creation_date=Faker().date_between(start_date=datetime.date(year=2015, month=1, day=1),
                                                                   end_date='+3y'),
                                author=random.choice(Author.objects.filter()),
                                views=0,
                                tags=[random.choice(Tag.objects.filter()) for i in range(5)]
                                )

        for i in range(Author.objects.count()):
            author = Author.objects[i]
            author.posts_count = Post.objects(author=author).count()
            author.save()

        print('!!! BLOG DB GENERATED !!!')


if __name__ == '__main__':
    BlogDataGenerator.generate_blog_data()
