from flask import Flask
from flask_restful import Api

from lesson10.practice.api.resources import BlogResource

app = Flask(__name__)
api = Api(app)

api.add_resource(BlogResource, '/posts')

if __name__ == '__main__':
    app.run(debug=True)