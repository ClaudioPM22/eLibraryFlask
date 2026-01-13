from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auths', __name__)

@auth_bp.route('/', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  token = AuthService.login(email,password)

  if not token:
    return jsonify({"message":"Credenciales invalidas"}), 401
  return jsonify({"access_token": token}), 200
