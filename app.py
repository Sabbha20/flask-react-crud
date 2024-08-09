from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import text,inspect
from flask_marshmallow import Marshmallow
import os
from pathlib import Path
import logging




# Load environment variables from .env file
load_dotenv(dotenv_path=Path('.') / '.env', override=True)
app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# print(f"connection url:\t{app.config['SQLALCHEMY_DATABASE_URI']}")
db = SQLAlchemy()
# Initialize the database with the app
db.init_app(app)
ma = Marshmallow(app)

# Import Users from models
from .models.models import Users, user_schema


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route("/useradd", methods=["POST"])
def useradd():
    name = request.json["name"]
    email = request.json["email"]
    
    users = Users(name, email)
    db.session.add(users)
    db.session.commit()
    
    # return jsonify({"success": "Successful Post"})
    return user_schema.jsonify(users)


from .db_conn_check import db_conn_check_bp
app.register_blueprint(db_conn_check_bp)

if __name__ == '__main__':
    app.debug = True
    app.run()