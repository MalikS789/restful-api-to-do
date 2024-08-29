from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from .auth import auth_bp
    from .tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
