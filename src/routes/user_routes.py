from flask import Blueprint, request, jsonify
from schemas import user_schema, users_schema
from services.user_service import UserService

user_bp = Blueprint('users', __name__)

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get_user(user_id):
  user = UserService.get_user_by_id(user_id)
  if not user:
    return jsonify({"message":"Usuario no encontrado"}), 404
  return jsonify(user_schema.dump(user)), 200

@user_bp.route('/', methods=['POST'])
def create_user():
  data = request.get_json()
  
  errors = user_schema.validate(data)
  if errors:
    return jsonify({"errors":errors}), 400
  
  try:
    user = UserService.create_user(data)
    return jsonify(user_schema.dump(user)), 201
  except ValueError as e:
    return jsonify({"error":str(e)}), 400
  

