from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.user import UserRole

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  email = fields.Str(required=True)
  password = fields.Str(required=True, load_only=True)
  role = EnumField(
    UserRole,
    by_value=True,
    dump_only=True
  )

  """role = fields.Str(
    validate = validate.OneOf(["admin","client"]),
    metadata = {"description":"El rol debe ser 'admin' o 'client'"}
  )"""