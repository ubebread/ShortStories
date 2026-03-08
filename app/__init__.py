# story_writer/app/__init__.py
import os
from flask import Flask
from .routes import main
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-insecure-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app