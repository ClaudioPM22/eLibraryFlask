from models.book import Book
from extensions import db

class BookService:
  @staticmethod
  def get_all_book():
    return Book.query.all()
  
  @staticmethod
  def get_book_by_id(book_id):
    return Book.query.get(book_id)
    
  @staticmethod
  def create_book(data):
    existing_isbn = Book.query.filter_by(isbn=data.get('isbn')).first()
    if existing_isbn:
      raise ValueError("El isbn ya existe.")
    
    new_book = Book(
      title=data.get('title'),
      author=data.get('author'),
      isbn=data.get('isbn'),
      numpages=data.get('numpages')
    )
    db.session.add(new_book)
    db.session.commit()
    return new_book
  
  @staticmethod
  def update_book(book_id, data):
    book= Book.query.get(book_id)
    if not book:
      return None
    book.title = data.get('title', book.title)
    book.author = data.get('author',book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.numpages = data.get('numpages',book.numpages)

    db.session.commit()
    return book
  
  @staticmethod
  def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
      db.session.delete(book)
      db.session.commit()
      return True
    return False
    