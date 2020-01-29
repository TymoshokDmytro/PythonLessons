from flask import request
from flask_restful import Resource

from lesson10.practice.api.models import Post, Author, Tag
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

    def put(self, post_id):
        if not post_id:
            return {'msg': 'post_id not defined for update'}
        pst = Post.objects.get(id=post_id)
        pst.modify(**request.json)
        return PostSchema().dump(pst)

    def delete(self, post_id):
        if not post_id:
            return {'msg': 'post_id not defined for update'}
        pst = Post.objects.get(id=post_id)
        author = pst.author
        author.posts_count -= 1
        author.save()
        pst.delete()
        return {'msg': 'deleted'}


class AuthorResource(Resource):
    def get(self, author_id):
        author = Author.objects.get(id=author_id)
        return PostSchema().dump(author.get_posts(), many=True)


class TagResource(Resource):
    def get(self, tag_id):
        tag = Tag.objects.get(id=tag_id)
        return PostSchema().dump(tag.get_posts(), many=True)
