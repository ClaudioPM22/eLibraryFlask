from models.loan import Loan, LoanStatus
from models.book import Book
from extensions import db
from datetime import date, timedelta

class LoanService:
  @staticmethod
  def check_book_available(book_id):
    active_loan = Loan.query.filter_by(book_id=book_id, status=LoanStatus.ACTIVE).first()

    return active_loan is None
  
  @staticmethod
  def calculate_return_date(numpages):
    if numpages <= 200:
      days = 7
    elif 200 < numpages <= 500:
      days = 14
    else:
      days = 21
    return date.today() + timedelta(days=days)
  
  @staticmethod
  def create_loan(data):
    book_id = data.get('book_id')
    user_id = data.get('user_id') 

    book = db.session.get(Book, book_id)
    if not book:
      raise Exception("El libro no existe.")
    
    if not LoanService.check_book_available(book_id):
      raise Exception("El libro ya está prestado.")

    due_date = LoanService.calculate_return_date(book.numpages)
    new_loan = Loan(
      book_id=book_id,
      user_id=user_id,
      return_date=due_date,
      status=LoanStatus.ACTIVE

    )

    db.session.add(new_loan)
    db.session.commit()
    return new_loan
  
  @staticmethod
  def return_book(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan or loan.status == LoanStatus.RETURNED:
      return None
    loan.mark_as_returned()
    db.session.commit()
    return loan
  