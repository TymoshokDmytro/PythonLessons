import random
from pprint import pprint

from mongoengine import *

from faker import Faker

from faker.providers import lorem, misc

connect('rest_homework_shop_db')

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(misc)


class Category(Document):
    title = StringField(min_length=1, max_length=255, required=True)
    description = StringField(max_length=4096)
    subcategories = ListField(ReferenceField('self'))
    parent = ReferenceField('self')
    is_root = BooleanField(default=False)

    @classmethod
    def create(cls, **kwargs):
        kwargs['subcategories'] = []
        if 'parent' in kwargs.keys() and kwargs['parent']:
            kwargs['is_root'] = False
        return cls(**kwargs).save()

    def add_subcategory(self, cat_obj):
        cat_obj.parent = self
        cat_obj.save()
        self.subcategories.append(cat_obj)
        self.save()

    def is_parent(self):
        return bool(self.parent)

    def get_products(self):
        return Product.objects.filter(category=self)

    def __str__(self):
        return f'{self.id}'


class Product(Document):
    title = StringField(min_length=1, max_length=255, required=True)
    category = ReferenceField(Category, required=True)
    description = StringField(max_length=4096)
    price = IntField(min_value=1, required=True)
    in_stock = IntField(min_value=0, default=0)
    views = IntField(min_value=0, default=0)

    def __str__(self):
        return f'{self.id}'


class RestShopDataGenerator:

    @staticmethod
    def generate_data():
        Category.drop_collection()
        Product.drop_collection()

        for i in range(3):
            root_category_dict = {
                'title': f'root_category_{i+1}',
                'description': f'the root category_{i+1}',
                'is_root': True,
            }

            root_category = Category.create(**root_category_dict)

            sub_categories = []
            for j in range(5):
                sub_category_dict = {
                    'title': f'sub_category_{j+1}[{i+1}]',
                    'description': f'the sub category_{j+1} of root_category_{j}',
                    'parent': root_category
                }
                sub_categories.append(Category(**sub_category_dict))

            Category.objects.insert(sub_categories)
            root_category.subcategories = Category.objects(parent=root_category)
            root_category.save()

        products = []
        for i in range(100):
            product_dict = {
                'title': f'product_{i}',
                'category': random.choice(Category.objects(is_root=False)),
                'description': fake.sentence(nb_words=6),
                'price': fake.random_int(min=0, max=9990, step=10),
                'in_stock': fake.random_int(min=5, max=100, step=1) if fake.boolean(
                    chance_of_getting_true=50) is True else 0
            }
            products.append(Product(**product_dict))

        Product.objects.insert(products)


if __name__ == '__main__':
    pass
    # RestShopDataGenerator.generate_data()

    # res = Product.objects.aggregate([
    #     {"$match": {"in_stock": {"$ne": 0}}},
    #     {'$group': {'_id': None, 'total': {'$sum': {'$multiply': ['$price', '$in_stock']}}}}
    # ]).next()
    #
    # pprint(res)
    #
    # res = Product.objects.aggregate([{"$match": {"in_stock": {"$ne": 0}}}])
    # print()
    #
    # sum = 0
    # for r in res:
    #     sum += r['in_stock'] * r['price']
    #     print(r['in_stock'], '*', r['price'], '=', r['in_stock'] * r['price'], ' | sum = ', sum)
