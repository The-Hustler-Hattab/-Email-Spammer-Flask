from flask import Flask
from dotenv import load_dotenv
import os
from flasgger import Swagger
from flask_cors import CORS


class Constants:
    DEBUG = 'DEBUG'
    MYSQL_URL = 'MYSQL_URL'
    TOGETHER_AI_API_KEY = 'TOGETHER_AI_API_KEY'


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set debug environment variable
app.config[Constants.DEBUG] = os.getenv(Constants.DEBUG)
app.config[Constants.MYSQL_URL] = os.getenv(Constants.MYSQL_URL)
app.config[Constants.TOGETHER_AI_API_KEY] = os.getenv(Constants.TOGETHER_AI_API_KEY)

# load swagger
swagger = Swagger(app)

CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*")
# Import routes after creating the app instance to avoid circular imports
from app import routes
