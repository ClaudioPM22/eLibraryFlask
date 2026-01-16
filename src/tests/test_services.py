from unittest.mock import patch
from services.loan_service import LoanService
from models import Book, User, Loan, LoanStatus
from datetime import date, timedelta
import pytest
from conftest import _db

# Test loan_service.py 

# Test return_date
def test_calculate_return_date_short_book(app):
  return_date = LoanService.calculate_return_date(100)
  expected_date = date.today() + timedelta(days=7)
  assert return_date == expected_date

def test_calculate_return_date_medium_book(app):
  return_date = LoanService.calculate_return_date(500)
  expected_date = date.today() + timedelta(days=14)
  assert return_date == expected_date

def test_calculate_return_date_long_book(app):
  return_date = LoanService.calculate_return_date(600)
  expected_date = date.today() + timedelta(days=21)
  assert return_date == expected_date

# Test create_loan
def test_create_loan(app,db):
  book = Book(id=1, title="Don Quijote", author="Julio", isbn="1234567890123",numpages=300)
  user = User(id=123, username="test001", email="test001@test.com",role="CLIENT", password="test001")
  db.session.add(user)
  db.session.add(book)
  db.session.commit()

  data = {'book_id':1, 'user_id':123}

  with patch.object(LoanService, 'check_book_available', return_value=True):
    loan = LoanService.create_loan(data)

  assert loan.id is not None
  assert loan.book_id == 1
  assert loan.user_id == 123
  assert loan.status == LoanStatus.ACTIVE
  assert loan.loan_date == date.today()
  assert loan.return_date == (date.today()+ timedelta(days=14))
  
def test_create_loan_book_not_found(app):
  data = {'book_id':1, 'user_id':1}
  with pytest.raises(Exception) as excinfo:
    LoanService.create_loan(data)

  assert "El libro no existe." == str(excinfo.value)

def test_create_loan_not_available(app,db):
  book = Book(id=1, title="Don Quijote", author="Julio", isbn="1234567890123",numpages=300)
  db.session.add(book)
  db.session.commit()
  
  data = {'book_id':1, 'user_id':123}

  with patch.object(LoanService,'check_book_available', return_value=False):
    with pytest.raises(Exception) as excinfo:
      LoanService.create_loan(data)

  assert str(excinfo.value) == "El libro ya está prestado." 

# Test return_book
def test_return_book_success(app,db):
  loan = Loan(book_id=1,user_id=1,loan_date=date.today(), return_date= date.today()+timedelta(days=7),status= LoanStatus.ACTIVE)
  db.session.add(loan)
  db.session.commit()

  returned_loan = LoanService.return_book(loan.id)

  assert returned_loan is not None
  assert returned_loan.status == LoanStatus.RETURNED

def test_return_book_not_found(app):
  result = LoanService.return_book(1)
  assert result is None
