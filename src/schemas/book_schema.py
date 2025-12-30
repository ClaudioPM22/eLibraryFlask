from marshmallow import Schema, fields

class BookSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  author = fields.Str(required=True)
  isbn = fields.Str(required=True)
  pages = fields.Int(required=True)