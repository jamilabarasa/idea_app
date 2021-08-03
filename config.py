from flask import Flask
import os

app = Flask(__name__)

db_path=os.path.join(os.path.dirname(__file__),'app.db')

db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["SECRET_KEY"]="GVAVAVABAVAVVAVAVAV"