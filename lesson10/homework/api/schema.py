from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.String()
    title = fields.String(min_length=1, max_length=255, required=True)
    description = fields.String(max_length=4096)
    subcategories = fields.List(fields.String, dump_only=True)
    parent = fields.String()
    is_root = fields.Bool(default=False)


class ProductSchema(Schema):
    id = fields.String()
    title = fields.String(min_length=1, max_length=255, required=True)
    category = fields.String(required=True)
    description = fields.String(max_length=4096)
    price = fields.Int(min_value=1, required=True)
    in_stock = fields.Int(min_value=0, default=0)
    views = fields.Int(min_value=0, default=0)
