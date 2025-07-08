# story_writer/app/__init__.py
from flask import Flask
from .routes import main, setup
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'e3b4f6de6f1d48a4b6fa3a2e5c3d4f7a9e6c4b2d1a0e8f5d3c7b6a1f9e2d0c3b'  # 👈 Add this line
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # 👈 initialize the database tables here

    return app