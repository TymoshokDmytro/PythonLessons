from mongoengine import *

connect('shop_db')


class Attributes(EmbeddedDocument):
    height = FloatField()
    weight = FloatField()
    width = FloatField()


class Cart(Document):
    user = StringField(max_length=32, required=True)
    is_archived = BooleanField(default=False)
    total = IntField(min_value=0, default=0)

    def get_size(self):
        return len(self.get_cart())

    def get_cart(self):
        return CartProduct.objects.filter(cart=self)

    def add_product_to_cart(self, product):
        CartProduct.objects.create(cart=self, product=product)
        self.total += product.get_price()
        self.save()

    def delete_product_from_cart(self, product):
        cart_prods = CartProduct.objects.filter(cart=self, product=product)
        if len(cart_prods) != 0:
            CartProduct.objects.filter(cart=self, product=product).first().delete()
            self.total -= product.get_price()
            self.save()

    def remove_product_from_cart(self, product):
        cart_prods = CartProduct.objects.filter(cart=self, product=product)
        if len(cart_prods) != 0:
            self.total -= product.get_price() * self.get_product_qty(product)
            self.save()
            CartProduct.objects.filter(cart=self, product=product).delete()

    def get_product_qty(self, product):
        return len(CartProduct.objects(cart=self, product=product))

    def remove_all_from_cart(self):
        CartProduct.objects(cart=self).delete()
        self.total = 0
        self.save()

    def get_total(self):
        return self.total

    def get_total_str(self):
        return str(round(self.total / 100, 2)) + ' UAH'


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
    img_url = StringField(max_length=1024)
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

    @staticmethod
    def get_price_str_repr(price):
        return str(round((price / 100), 2))

    def get_price_str(self):
        return self.get_price_str_repr(self.get_price()) + ' UAH'

    def get_price_markdown_str(self):
        if self.discount_price:
            return f"<s>{self.get_price_str_repr(self.price)}</s> <b>{self.get_price_str_repr(self.discount_price)}</b> UAH"
        return self.get_price_str()

    def get_total_str(self, qty):
        return str(round(((self.get_price() * qty) / 100), 2)) + ' UAH'

# if __name__ == '__main__':
#     Cart.drop_collection()
#     CartProduct.drop_collection()
