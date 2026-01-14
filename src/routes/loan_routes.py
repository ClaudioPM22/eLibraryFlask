from flask import Blueprint, request, jsonify
from schemas import loan_schema, loans_schema
from services.loan_service import LoanService
from flask_jwt_extended import jwt_required

loan_bp = Blueprint('loans', __name__)

@loan_bp.route('/check/<int:book_id>', methods=['GET'])
def check_available(book_id):
  is_available = LoanService.check_book_available(book_id)
  return jsonify({"book_id":book_id, "available":is_available}), 200
  
@loan_bp.route('/', methods=['POST'])
@jwt_required()
def create_loan():
  data = request.get_json()

  errors = loan_schema.validate(data)
  if errors:
    return jsonify({"errors":errors}), 400
  try:
    loan = LoanService.create_loan(data)
    return jsonify(loan_schema.dump(loan)), 201 #Para created
  except Exception as e:
    return jsonify({"error":str(e)}), 400

@loan_bp.route('/<int:loan_id>/return', methods=['PUT'])
@jwt_required()
def return_book(loan_id):
  try:
    loan = LoanService.return_book(loan_id)
    if not loan:
      return jsonify({"message":"Prestamo no encontrado o ya devuelto"}), 404
    
    return jsonify({
      "message":"Libro devuelto exitosamente",
      "loan":loan_schema.dump(loan)
    }), 200
  except Exception as e:
    return jsonify({"error":str(e)}), 500

