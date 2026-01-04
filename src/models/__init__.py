from extensions import db
from .book import Book
from .user import User
from .loan import Loan

# Esto permite que otros archivos importen todo desde 'models'
__all__ = ["Book", "User", "Loan"]