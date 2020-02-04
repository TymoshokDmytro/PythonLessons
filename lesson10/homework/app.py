from flask import Flask
from flask_restful import Api

from lesson10.homework.api.resources import CategoryResource, ProductResource, TotalResource

app = Flask(__name__)
api = Api(app, prefix='/v1')

api.add_resource(CategoryResource, '/categories', '/categories/<string:cat_id>')
api.add_resource(ProductResource, '/product', '/product/<string:product_id>')
api.add_resource(TotalResource, '/total')

if __name__ == '__main__':
    app.run(debug=True)
