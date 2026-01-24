import pytest
from app import create_app
from extensions import db as _db
from models import Book, User, Loan
import pytest
from flask_jwt_extended import create_access_token
from models import UserRole

@pytest.fixture
def app():
  app = create_app()
  app.config.update({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "JWT_SECRET_KEY": "test-secret-key",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,    
  })
  with app.app_context():
    _db.create_all()
    yield app
    _db.drop_all()

@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def db(app):
  return _db

@pytest.fixture
def sample_books(db):
  book1 = Book(
    title="Libro de prueba 1",
    author="test1",
    isbn="1234567890123",
    numpages=400,
  )
  book2 = Book(
    title="Libro de prueba 2",
    author="test1",
    isbn="1234567891012",
    numpages=200,
  )
  db.session.add_all([book1,book2])
  db.session.commit()
  return [book1,book2]

@pytest.fixture
def sample_users(db):
  user1 = User(
    username="tester001",
    email="tester001@test.com",
    role=UserRole.CLIENT,
  )
  user1.set_password("tester001")
  user2 = User(
    username="tester002",
    email="tester002@test.com",
    role=UserRole.CLIENT,
  )
  user2.set_password("tester002")
  db.session.add_all([user1,user2])
  db.session.commit()
  return [user1,user2]

@pytest.fixture
def sample_loans(db):
  loan1= Loan(
    user_id = 1,
    book_id = 1
  )
  db.session.add(loan1)
  db.session.commit()
  return loan1
  

@pytest.fixture
def auth_headers(app):
  with app.app_context():
    token = create_access_token(identity="1")
    return {
        "Authorization": f"Bearer {token}"
    }
