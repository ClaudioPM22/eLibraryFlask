from .book_schema import BookSchema
from .loan_schema import LoanSchema
from .user_schema import UserSchema

book_schema = BookSchema()
books_schema = BookSchema(many=True)

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)