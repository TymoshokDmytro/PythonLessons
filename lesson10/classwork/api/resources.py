from flask import request, Response
from flask_restful import Resource
from .schema import *
from .models import *


class DeveloperResource(Resource):

    def get(self, dev_id=None):
        query = Developer.objects if not dev_id else Developer.objects.get(id=dev_id)
        many = not dev_id

        return DeveloperSchema().dump(query, many=many)

    def post(self):
        err = DeveloperSchema().validate(request.json)

        if err:
            return err
        dev = Developer(**request.json).save()
        return DeveloperSchema().dump(dev)

    def put(self):
        return 'put'

    def delete(self):
        return 'delete'
