from functools import wraps
from authlib.jose import jwt
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flasgger import Swagger
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from security import safe_requests


class Constants:
    DEBUG = 'DEBUG'
    MYSQL_URL = 'MYSQL_URL'
    TOGETHER_AI_API_KEY = 'TOGETHER_AI_API_KEY'
    OIDC_JWK_URL = 'OIDC_JWK_URL'


app = Flask(__name__)
oauth = OAuth(app)

# Load environment variables from .env file
load_dotenv()

# Set debug environment variable
app.config[Constants.DEBUG] = os.getenv(Constants.DEBUG)
app.config[Constants.MYSQL_URL] = os.getenv(Constants.MYSQL_URL)
app.config[Constants.TOGETHER_AI_API_KEY] = os.getenv(Constants.TOGETHER_AI_API_KEY)
app.config[Constants.OIDC_JWK_URL] = os.getenv(Constants.OIDC_JWK_URL)
# load swagger
swagger = Swagger(app)

CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*")

OKTA_JWK_URL = app.config.get(Constants.OIDC_JWK_URL)


def get_okta_public_keys():
    response = safe_requests.get(OKTA_JWK_URL)
    response.raise_for_status()
    return response.json()['keys']


keys = get_okta_public_keys()


def verify_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid token format'}), 401

        token = token.split(' ')[1]

        # Try decoding token using each key until successful
        for key in keys:
            try:
                jwt.decode(token, key)

                # If token is valid, proceed with the request
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                # Ignore any errors during decoding and try the next key
                pass

        # If none of the keys succeeded in decoding the token, return an error
        return jsonify({'message': 'Invalid token'}), 401

    return decorated_function
