from config import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profileImageUrl = db.Column(db.String(200),unique=True,nullable=False)
    gender = db.Column(db.Enum("MALE","FEMALE","RATHER_NOT_SAY"),nullable=False)

    def __repr__(self) -> str:
        return "<Member %r>" % self.name

    @property
    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'profileImageUrl':self.profileImageUrl,
            'gender':self.gender
        }


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime,nullable=False,default=datetime.now())

    def __repr__(self) -> str:
        return "<Team %r>" % self.name

    @property
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'creation_date':self.creation_date
        }

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    role = db.Column(db.String,nullable=False)

    def __repr__(self) -> str:
        return "<Family %r>" % self.name

    @property
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'role':self.role
        }    
