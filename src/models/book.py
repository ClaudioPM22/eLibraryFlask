from extensions import db

class Book(db.Model):
  __tablename__ = "books"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  author = db.Column(db.String(100), nullable=False)
  isbn = db.Column(db.String(13), unique=True, nullable=False)
  numpages = db.Column(db.Integer,nullable=False)