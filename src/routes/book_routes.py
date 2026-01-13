from flask import Blueprint, request, jsonify
from schemas import book_schema, books_schema
from services.book_service import BookService
from flask_jwt_extended import jwt_required

book_bp = Blueprint('books', __name__)


@book_bp.route('/', methods=['GET'])
def get_books():
  books = BookService.get_all_book()
  return jsonify(books_schema.dump(books)), 200

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
  book = BookService.get_book_by_id(book_id)
  if not book:
    return jsonify({"message": "Libro no encontrado"}), 404
  return jsonify(book_schema.dump(book)), 200

@book_bp.route('/', methods=['POST'])
@jwt_required()
def create_book():
  data = request.get_json()
  
  #Validando datos con schema
  errors = book_schema.validate(data)
  if errors:
    return jsonify({"errors": errors}), 400
  
  try:
    # Llamamos al servicio
    new_book = BookService.create_book(data)
    return jsonify(book_schema.dump(new_book)), 201
  except ValueError as e:
    return jsonify({"error": str(e)}), 400

@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
  data = request.get_json()

  errors = book_schema.validate(data)
  if errors:
    return jsonify({"errors":errors}), 400
  
  up_book = BookService.update_book(book_id,data)
  if not up_book:
    return jsonify({"message":"Libro no encontrado"}), 404
  
  return jsonify(book_schema.dump(up_book)), 200

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
  success = BookService.delete_book(book_id)
  if not success:
    return jsonify({"message":"Libro no encontrado"}), 404
  return jsonify({"message":"Libro eliminado correctamente"}), 200
  