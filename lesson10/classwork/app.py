import json

from flask import Flask, render_template, jsonify, request, Response
from flask_restful import Api

from lesson10.classwork.api import models
from lesson10.classwork.api.resources import DeveloperResource

app = Flask(__name__)
api = Api(app)

api.add_resource(DeveloperResource, '/developers', '/developers/<string:dev_id>')

# @app.route('/developers', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def developers():
#
#
#     if request.method == 'GET':
#         json_str = models.Developer.objects.to_json()
#         return Response(json_str, mimetype='application/json')
#
#     elif request.method == 'POST':
#         models.Developer(
#             **request.json
#         ).save()
#         return Response(status=200)
#
#     elif request.method == 'PUT':
#         return Response(status=666)
#
#     elif request.method == 'DELETE':
#         return Response(status=999)


if __name__ == '__main__':
    app.run(debug=True)
