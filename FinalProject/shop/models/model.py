from mongoengine import *

connect('shop_db')


class Attributes(EmbeddedDocument):
    height = FloatField()
    weight = FloatField()
    width = FloatField()


class User(Document):
    telegram_id = StringField(max_length=32, required=True)
    username = StringField(max_length=128)
    fullname = StringField(max_length=256)
    phone = StringField(max_length=20)
    email = EmailField()


class Cart(Document):
    user = ReferenceField(User)
    is_archived = BooleanField(default=False)

    def get_cart(self):
        return CartProduct.objects.filter(cart=self)

    # TODO Overthink
    # def get_sum(self):
    #     pass


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
        if kwargs['parent']:
            kwargs['is_root'] = False
        Product(**kwargs).save()

    def add_subcategory(self, cat_obj):
        cat_obj.parent = self
        cat_obj.save()
        self.subcategories.append(cat_obj)
        self.subcategories.save()

    def is_parent(self):
        return bool(self.parent)

    def get_products(self):
        return Product.objects.filter(category=self)


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

category_dict={
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

        for i in range(category_num):
            # title = StringField(min_length=1, max_length=255, required=True)
            # description = StringField(max_length=4096)
            # subcategories = ListField(ReferenceField('self'))
            # parent = ReferenceField('self')
            # is_root = BooleanField(default=False)
            Category.objects.create(
                title=fake.random_choices(elements=('a', 'b', 'c'))
                description =
                subcategories =
                parent =
                is_root =
            )

if __name__ == '__main__':
    ShopDataGenerator.generate_data()
    pass
