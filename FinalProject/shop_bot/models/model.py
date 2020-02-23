from pprint import pprint

from mongoengine import *

connect('shop_db')


class Attributes(EmbeddedDocument):
    height = FloatField()
    weight = FloatField()
    width = FloatField()


class User(Document):
    choises = (
        ('products', 'products'),
        ('categories', 'categories')
    )

    telegram_id = StringField(max_length=32, required=True)
    username = StringField(max_length=128)
    fullname = StringField(max_length=256)
    phone = StringField(max_length=20)
    state = StringField(choices=choises)
    email = EmailField()


class Cart(Document):
    user = ReferenceField(User)
    is_archived = BooleanField(default=False)

    def get_cart(self):
        return CartProduct.objects.filter(cart=self)

    def add_product_to_cart(self, product):
        CartProduct.objects.create(cart=self, product=product)

    def delete_product_from_cart(self, product):
        CartProduct.objects.filter(cart=self, product=product).first().delete()

class CartProduct(Document):
    cart = ReferenceField(Cart)
    product = ReferenceField('Product')


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
        return self.title


class Product(Document):
    title = StringField(min_length=1, max_length=255, required=True)
    category = ReferenceField(Category, required=True)
    article = StringField(max_length=32, required=True)
    description = StringField(max_length=4096)
    price = IntField(min_value=1, required=True)
    in_stock = IntField(min_value=0, default=0)
    discount_price = IntField(min_value=1)
    attributes = EmbeddedDocumentField(Attributes)
    extra_data = StringField()

    def get_price(self):
        return self.price if not self.discount_price else self.discount_price


class Texts(Document):
    TEXT_TYPES = (
        ('Greetings', 'Greetings'),
        ('News', 'News')
    )
    text_type = StringField(choices=TEXT_TYPES)
    body = StringField(max_length=2048)


category_dict = {
    'Toys': [],
    'Equipment': [],
    'Office Tools': [],
    'Computers': [],
    'Large House electronics': [],
    'Small house electronics': [],
    'Phones': [],
    'Plumbing': [],
    'Television': [],
    'Tires': []
}


class ShopDataGenerator:

    @staticmethod
    def generate_data(user_num=5, category_num=10):
        from faker import Faker
        from faker.providers import person, internet
        fake = Faker()
        fake.add_provider(person)
        fake.add_provider(internet)

        Category.drop_collection()
        User.drop_collection()
        Cart.drop_collection()
        Product.drop_collection()

        for i in range(user_num):
            User.objects.create(telegram_id=fake.numerify(text='#########'),
                                username=fake.last_name(),
                                fullname=fake.name(),
                                phone=fake.numerify(text='+3809########'),
                                email=fake.ascii_email())

        root_category_dict = {
            'title': 'category_root',
            'description': 'category_root description',
            'is_root': True
        }

        root_cat = Category.create(**root_category_dict)
        for i in range(category_num):
            category_dict = {
                'title': f'category{i}',
                'description': f'category{i} description'
            }
            sub_cat = Category(**category_dict)
            root_cat.add_subcategory(sub_cat)


if __name__ == '__main__':
    # ShopDataGenerator.generate_data()

    # Category.drop_collection()
    # category_dict = {
    #     'title': 'category_root',
    #     'description': 'category_root description',
    #     'is_root': True
    # }
    #
    # root_cat = Category.create(**category_dict)
    # for i in range(5):
    #     category_dict = {
    #         'title': f'category{i}',
    #         'description': f'category{i} description'
    #     }
    #     sub_cat = Category(**category_dict)
    #     root_cat.add_subcategory(sub_cat)

    # root = Category.objects(is_root=True)
    #
    # for cat in root:
    #     print(cat)
    #
    #     if cat.subcategories:
    #         for sub in cat.subcategories:
    #             print(f'Parent is {sub.parent}')
    #             print(f'Sub cat is {sub}')
    #             print()

    # User.drop_collection()
    # Cart.drop_collection()
    # CartProduct.drop_collection()
    # Product.drop_collection()
    # user = User.objects.create(telegram_id='123456')
    # cart = Cart.objects.create(user=user)
    # USE insert with list of Objects

    # cart = Cart.objects.first()


    # products = []
    # for i in range(10):
    #     product = {
    #         'title': f'product{i}',
    #         'article': f'arcticle{i}',
    #         'category': Category.objects.first(),
    #         'price': 10 * (i+1)
    #     }
    #     created_product = Product.objects.create(**product)
    #     cart.add_product_to_cart(created_product)
    #
    # pprint(cart.get)
    # Product.objects.insert(products)

    cart = Cart.objects.first()
    frequencies = cart.get_cart().item_frequencies('product')
    print(frequencies)

