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
    article = StringField(max_length=64, required=True)
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

