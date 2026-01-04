from models.loan import Loan
from models.book import Book
from models.user import User
from extensions import db
from datetime import datetime

class LoanService:
  @staticmethod
  def check_book_available(book_id):
    active_loan = Loan.query.filter_by(book_id=book_id, return_date=None).first()

    if active_loan:
      return False # No está disponible
    return True # Esta disponible
  
  @staticmethod
  def create_loan(data):
    book_id = data.get('book_id')
    # Vemos si esta disponible
    if not LoanService.check_book_available(book_id):
      raise Exception("El libro ya se encuentra prestado actualmente.")
    # Si esta disponible, creamos el registro
    new_loan = Loan(
      book_id=book_id,
      user_id=data.get('user_id ')
    )

    db.session.add(new_loan)
    db.session.commit()
    return new_loan