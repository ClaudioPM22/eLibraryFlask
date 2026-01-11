from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.loan import LoanStatus
##from extensions import ma

class LoanSchema(Schema):
  id = fields.Int(dump_only=True)
  loan_date = fields.Date(dump_only=True)
  return_date = fields.Date(dump_only=True)

  user_id = fields.Int(required=True, error_messages={"required": "El ID de usuario es obligatorio."})
  book_id = fields.Int(required=True, error_messages={"required": "El ID del libro es obligatorio."})
  status = EnumField(LoanStatus, by_value=True, dump_only=True)
