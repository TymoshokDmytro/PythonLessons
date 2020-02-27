import datetime
import logging
import os

from flask import Flask
from flask_restful import Api

from api.resources import CategoryResource, ProductResource

app = Flask(__name__)
api = Api(app, prefix='/bot/v1')

api.add_resource(CategoryResource, '/category', '/category/<string:cat_id>')
api.add_resource(ProductResource, '/product', '/product/<string:product_id>')

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/log_' + datetime.date.today().strftime("%Y_%m_%d") + '_api.log',
                        datefmt="%Y_%m_%d %H:%M:%S",
                        level=logging.DEBUG)
    app.run(host='127.0.0.1', port=5000, debug=True)
