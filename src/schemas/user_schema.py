from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from models.user import UserRole

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True, validate=validate.Length(min=3))
  email = fields.Email(required=True, error_messages={"invalid": "Formato de correo inválido."})
  password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
  role = EnumField(
    UserRole,
    by_value=True
  )

  """role = fields.Str(
    validate = validate.OneOf(["admin","client"]),
    metadata = {"description":"El rol debe ser 'admin' o 'client'"}
  )"""