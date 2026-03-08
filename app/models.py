# story_writer/app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(64), nullable=False, index=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def for_session(session_id):
        return Story.query.filter_by(user_session=session_id).order_by(Story.created_at.desc()).all()