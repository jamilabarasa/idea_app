from config import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profileImageUrl = db.Column(db.String(200),unique=True,nullable=False)

    def __repr__(self) -> str:
        return "<Member %r>" % self.name

    @property
    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'profileImageUrl':self.profileImageUrl
        }


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime,nullable=False,default=datetime.now())
    members = db.Column(db.PickleType,nullable=False)

    def __repr__(self) -> str:
        return "<Team %r>" % self.name

    @property
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'creation_date':self.creation_date,
            'members':self.members
        }
