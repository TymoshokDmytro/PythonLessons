from flask import request
from flask_restful import Resource

from lesson10.practice.api.models import Post, Author
from lesson10.practice.api.schema import PostSchema, AuthorSchema


class PostsResource(Resource):

    def get(self, post_id=None):
        query = Post.objects if not post_id else Post.objects.get(id=post_id)
        many = not post_id
        if not many:
            query.views += 1
            query.save()
        return PostSchema().dump(query, many=many)

    def post(self):
        err = PostSchema().validate(request.json)

        if err:
            return err
        pst = Post(**request.json).save()
        return PostSchema().dump(pst)


#
# def put(self):
#     return 'put'
#
# def delete(self):
#     return 'delete'

class AuthorResource(Resource):
    pass
