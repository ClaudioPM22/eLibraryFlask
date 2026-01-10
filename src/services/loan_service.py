from models.loan import Loan
from .book_service import BookService
from .user_service import UserService
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
    user_id = data.get('user_id') 

    if not BookService.get_book_by_id(book_id):
        raise Exception("Operación fallida: El libro no existe en el sistema.")
    
    if not UserService.get_user_by_id(user_id):
        raise Exception("Operación fallida: El usuario no está registrado.")

    if not LoanService.check_book_available(book_id):
        raise Exception("El libro ya se encuentra prestado actualmente.")
    
    new_loan = Loan(
      book_id=book_id,
      user_id=data.get('user_id')
    )

    db.session.add(new_loan)
    db.session.commit()
    return new_loan
  
  @staticmethod
  def return_book(loan_id):
     loan = Loan.query.get(loan_id)
     if not loan or loan.return_date is not None:
        return None
     loan.return_date = datetime.now()
     db.session.commit()
     return loan
  