from models.user import User, UserRole
from extensions import db

class InvalidRoleError(Exception):
  pass

class UserService:
  @staticmethod
  def get_user_by_id(user_id):
    return db.session.get(User, user_id)
  
  @staticmethod
  def create_user(data):
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
      raise ValueError("El correo electronico ya esta registrado.")
    
    role_str = data.get("role","client")
    try:
      role_enum = UserRole(role_str)
    except ValueError:
      raise InvalidRoleError("Rol invalido")
    
    new_user = User(
      username=data.get('username'),
      email=data.get('email'),
      role= role_enum,
    )
    new_user.set_password(data.get('password'))
    
    db.session.add(new_user)
    db.session.commit()
    return new_user