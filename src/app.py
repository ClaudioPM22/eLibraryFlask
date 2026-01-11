import os
from dotenv import load_dotenv
from flask import Flask
from models import Book, User, Loan
from routes import book_bp, user_bp, loan_bp
from extensions import db, migrate, ma

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    # Registro de Blueprints con un prefijo de URL
    app.register_blueprint(book_bp, url_prefix='/api/books')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(loan_bp, url_prefix='/api/loans')

    return app

# El punto de entrada para ejecutar la app
if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5000)
