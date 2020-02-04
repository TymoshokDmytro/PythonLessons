from flask import request
from flask_restful import Resource

from lesson10.homework.api.models import Category, Product
from lesson10.homework.api.schema import CategorySchema, ProductSchema


class CategoryResource(Resource):

    def get(self, cat_id=None):
        many = not cat_id
        query = Category.objects.get(id=cat_id) if cat_id else Category.objects()

        return CategorySchema().dump(query, many=many)

    def post(self):
        err = CategorySchema().validate(request.json)

        if err:
            return err
        cat = Category(**request.json).save()
        return CategorySchema().dump(cat)

    def put(self, cat_id):
        if not cat_id:
            return {'msg': 'cat_id not defined for update'}
        cat = Category.objects.get(id=cat_id)
        cat.modify(**request.json)
        return CategorySchema().dump(cat)

    def delete(self, cat_id):
        if not cat_id:
            return {'msg': 'cat_id not defined for update'}
        Category.objects.get(id=cat_id).delete()
        return {'msg': 'deleted'}


class ProductResource(Resource):

    def get(self, product_id=None):
        many = not product_id
        query = Product.objects.get(id=product_id) if product_id else Product.objects()

        return ProductSchema().dump(query, many=many)

    def post(self):
        err = ProductSchema().validate(request.json)

        if err:
            return err
        product = Product(**request.json).save()
        return ProductSchema().dump(product)

    def put(self, product_id):
        if not product_id:
            return {'msg': 'cat_id not defined for update'}
        product = Product.objects.get(id=product_id)
        product.modify(**request.json)
        return ProductSchema().dump(product)

    def delete(self, product_id):
        if not product_id:
            return {'msg': 'cat_id not defined for update'}
        Product.objects.get(id=product_id).delete()
        return {'msg': 'deleted'}


class TotalResource(Resource):
    def get(self):
        total = Product.objects.aggregate([
            {"$match": {"in_stock": {"$ne": 0}}},
            {'$group': {'_id': None, 'total': {'$sum': {'$multiply': ['$price', '$in_stock']}}}}
        ]).next()

        return {'total': total['total']}
