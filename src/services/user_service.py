from models.user import User
from extensions import db

class UserService:
  @staticmethod
  def get_user_by_id(user_id):
    return User.query.get(user_id)
  
  @staticmethod
  def create_user(data):
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
      raise ValueError("El correo electrónico ya esta registrado.")
    
    new_user = User(
      username=data.get('username'),
      email=data.get('email'),
      password=data.get('password'),
      role=data.get('role')
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user