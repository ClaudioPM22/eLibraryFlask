from extensions import db
from sqlalchemy import ForeignKey, Date
from datetime import date, timedelta
import enum
class LoanStatus(enum.Enum):
  ACTIVE = "active"
  RETURNED = "returned"
  OVERDUE = "overdue"
  #NONE = "none" Nunca se ha prestado se elimina, dado que si nunca se presto no existe un loan

class Loan(db.Model):
  __tablename__ = "loans"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(
    db.Integer,
    ForeignKey("users.id"),
    nullable = False
    )
  book_id = db.Column(
    db.Integer,
    ForeignKey("books.id"),
    nullable = False
  )
  loan_date = db.Column(
    Date, 
    default = date.today,
    nullable = False
  )
  return_date = db.Column(
    Date,
    nullable = False
  )
  status = db.Column(
    db.Enum(LoanStatus),
    default = LoanStatus.ACTIVE,
    nullable = False
  )

  user = db.relationship("User", backref="loans")
  book = db.relationship("Book", backref="loans")

  def __repr__(self):
    return f"<Loan book={self.book_id} user={self.user_id} status={self.status.value}>"
  
  def mark_as_returned(self):
    self.status = LoanStatus.RETURNED
  
  def is_overdue(self):
    return self.return_date < date.today() and self.status == LoanStatus.ACTIVE
  
  def renew(self, extra_days):
    self.return_date += timedelta(days=extra_days)