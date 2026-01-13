from flask_jwt_extended import create_access_token
from models.user import User

class AuthService:
  @staticmethod
  def login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
      access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role.value})

      return access_token
    return None