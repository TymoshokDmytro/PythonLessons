import json
from pprint import pprint

from mongoengine import *


class Products(Document):
    title = StringField(max_length=255)
    description = StringField(max_length=2048)
    price = DecimalField(min_value=0)


class User(Document):
    login = StringField(min_length=8, max_length=255, required=True)
    password = StringField(min_length=8, required=True)
    fullname = StringField(max_length=255, min_length=3)
    bill = DecimalField(min_value=0)
    number = IntField()
    wishes = ListField(ReferenceField(Products))

    def __str__(self):
        return self.fullname

    def get_user_wishes(self):
        return self.wishes


if __name__ == '__main__':
    connect('db_exmp')
    # user = User.objects.create(
    #     fullname='Andriy Khohlov',
    #     login='akhohlov',
    #     password='12345678',
    #     bill=666.66,
    #     number=231
    # )

    # product_phone = Products(
    #     title='IPhone 11',
    #     description='This is phone',
    #     price=19000
    # ).save()
    #
    # product_car = Products(
    #     title='Chevrolet Aveo',
    #     description='This is car',
    #     price=60000
    # ).save()

    # products = Products.objects

    # user = User.objects.get(fullname="Andriy Khohlov")
    # user.wishes = [
    #     product_car,
    #     product_phone
    # ]
    # user.save()

    user = User.objects.get(login='akhohlov')
    print(user.get_user_wishes())

    # pprint(json.loads(user.to_json()))

    # users = User.objects.filter(fullname__ne="Andriy Khohlov")
    #
    # for user in users:
    #     print(user.fullname)
    #
    # json_users = json.loads(users.to_json())
    # pprint(json_users)
