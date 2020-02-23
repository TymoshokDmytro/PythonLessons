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


categories_json = {
    'Phones': {
        'Stationary': {
            'Panasonic': {},
            'VTech': {}
        },
        'Mobile': {
            'Samsung': {},
            'Xiaomi': {},
            'Nokia': {}
        }
    },
    'Cpu': {
        'Intel': {},
        'AMD': {}
    }
}

categories_description_dict = {
    'Phones': 'Category of Phones',
    'Stationary': 'Stationary DECT phones',
    'Panasonic': 'Category of Panasonic stationary phones',
    'VTech': 'Category of VTech stationary phones',
    'Mobile': 'Mobile phones',
    'Samsung': 'Samsung phones',
    'Xiaomi': 'Xiaomi phones',
    'Nokia': 'Nokia phones',
    'Cpu': "Category of cpu's",
    'Intel': "Category of Intel cpu's",
    'AMD': "Category of AMD cpu's"
}

panasonic_cat_id = str(Category.objects(title='Panasonic').get().id)

products_dict = {
    'Panasonic_1': {
        'title': 'Panasonic KX-TGE43B',
        'category': panasonic_cat_id,
        'article': 'KX-TGE43B',
        'description': 'Expandable Cordless Phone System with Answering Machine ',
        'price': 6995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_2': {
        'title': 'Panasonic KX-TGE434B',
        'category': panasonic_cat_id,
        'article': 'KX-TGE434B',
        'description': 'Expandable Cordless Phone System with Answering Machine - 4 Handsets - KX-TGE434B',
        'price': 10995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_3': {
        'title': 'Panasonic KX-TGE484S2',
        'category': panasonic_cat_id,
        'article': 'KX-TGE484S2',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Rugged Phone - 4 Handsets - KX-TGE484S2',
        'price': 15995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_4': {
        'title': 'Panasonic KX-TGC364B',
        'category': panasonic_cat_id,
        'article': 'KX-TGC364B',
        'description': 'Expandable Cordless Phone with Answering System - 4 Handsets - KX-TGC364B',
        'price': 8995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_5': {
        'title': 'Panasonic KX-TGD583M2',
        'category': panasonic_cat_id,
        'article': 'KX-TGD583M2',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Voice Assist and Answering Machine Standard Handset + Rugged Phone Series - KX-TGD58M2',
        'price': 11995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_6': {
        'title': 'Panasonic KX-TGD563M',
        'category': panasonic_cat_id,
        'article': 'KX-TGD563M',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Voice Assist and Answering Machine - KX-TGD56M Series',
        'price': 10995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_7': {
        'title': 'Panasonic KX-TGD562G',
        'category': panasonic_cat_id,
        'article': 'KX-TGD562G',
        'description': 'Link2Cell Bluetooth Cordless Phone with Answering Machine - KX-TGD56 Series',
        'price': 8995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_8': {
        'title': 'Panasonic KX-TGD510B',
        'category': panasonic_cat_id,
        'article': 'KX-TGD510B',
        'description': 'Expandable Cordless Phone with Call Block - KX-TGD51 Series',
        'price': 6995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_9': {
        'title': 'Panasonic KX-TGE474S',
        'category': panasonic_cat_id,
        'article': 'KX-TGE474S',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Large Keypad- KX-TGE47 Series',
        'price': 14995,
        'in_stock': 1,
        'discount_price': 0
    },
    'Panasonic_10': {
        'title': 'Panasonic KX-TGM450S',
        'category': panasonic_cat_id,
        'article': 'KX-TGM450S',
        'description': 'Amplified Cordless Phone with Digital Answering Machine - 1 Handset - KX-TGM450S',
        'price': 15995,
        'in_stock': 1,
        'discount_price': 0
    }

}


def recursive_categories_creation(cat_json, previous_cat=None, level=0):
    for key, value in cat_json.items():

        root_category_dict = {
            'title': key,
            'description': categories_description_dict[key],
            'is_root': True if level == 0 else False
        }

        category = Category.create(**root_category_dict)
        if previous_cat:
            previous_cat.add_subcategory(category)

        if value:
            recursive_categories_creation(cat_json[key], category, level=level + 1)


# cart = Cart.objects.first()
# frequencies = cart.get_cart().item_frequencies('product')
# print(frequencies)

if __name__ == '__main__':
    pass
    # ShopDataGenerator.generate_data()

    # Category.drop_collection()
    # recursive_categories_creation(categories_json)

    pprint(products_dict)
