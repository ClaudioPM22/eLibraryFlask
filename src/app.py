import os
from dotenv import load_dotenv
from flask import Flask
from models import Book, User, Loan
from extensions import db, migrate

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app
