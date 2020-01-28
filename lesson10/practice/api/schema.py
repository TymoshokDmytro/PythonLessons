from marshmallow import fields, Schema, validates, ValidationError


class TagSchema(Schema):
    tag = fields.String(max_length=16, required=True)


class AuthorSchema(Schema):
    fullname = fields.String(max_length=64, required=True)
    posts_count = fields.Int(min_value=0)


class PostSchema(Schema):
    title = fields.String(max_length=64, required=True)
    description = fields.String(max_length=8192, required=True)
    creation_date = fields.DateTime(required=True)
    author = AuthorSchema
    views = fields.Int(min_value=0, required=True)
    tag = fields.Nested(TagSchema, dump_only=True)
