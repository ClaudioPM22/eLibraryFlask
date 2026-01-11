from marshmallow import Schema, fields, validate
#from extensions import ma ##Para futuras actualizaciones


class BookSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True, validate=validate.Length(min=1))
  author = fields.Str(required=True)
  isbn = fields.Str(required=True, validate=validate.Length(equal=13))
  numpages = fields.Int(required=True)

