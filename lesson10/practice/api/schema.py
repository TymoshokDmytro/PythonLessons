import datetime

from marshmallow import fields, Schema, validates, ValidationError


class TagSchema(Schema):
    id = fields.String()
    tag = fields.String(max_length=16, required=True)

    @validates('tag')
    def val_tag(self, value):
        if type(value) is not str:
            raise ValidationError('Tag type must str')
        if value and value[0] != '#':
            raise ValidationError('Tag must starts with #')


class AuthorSchema(Schema):
    id = fields.String()
    fullname = fields.String(max_length=64, required=True)
    posts_count = fields.Int(min_value=0)

    @validates('fullname')
    def val_fullname(self, value):
        if len(value) > 64:
            raise ValidationError('Fullname must be < 64 length')


class PostSchema(Schema):
    id = fields.String()
    title = fields.String(max_length=64, required=True)
    description = fields.String(max_length=8192, required=True)
    creation_date = fields.DateTime(default=datetime.datetime.now())
    author = fields.Nested(AuthorSchema)
    views = fields.Int(min_value=0, default=0)
    tags = fields.List(fields.Nested(TagSchema, dump_only=True))
