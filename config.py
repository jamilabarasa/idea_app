from flask import Flask
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db_path=os.path.join(os.path.dirname(__file__),'app.db')

db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'


# from environment
AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI")
BASE_URI = os.environ.get("FN_BASE_URI")
CLIENT_ID = os.environ.get("FN_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET")
LANDING_URI =os.environ.get("FN_LANDING_URI")

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'