# story_writer/app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())