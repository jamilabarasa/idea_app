from enum import unique
from config import app
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profileImageUrl = db.Column(db.String(200),unique=True,nullable=False)
    gender = db.Column(db.Enum("MALE","FEMALE","RATHER_NOT_SAY"),nullable=False)

    def __repr__(self) -> str:
        return "<Member %r>" % self.name