from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text
import os
from pathlib import Path

# Load environment variables from .env file
load_dotenv(dotenv_path=Path('.') / '.env', override=True)
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# print(f"connection url:\t{app.config['SQLALCHEMY_DATABASE_URI']}")

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/useradd", methods=["POST"])
def useradd():
    name = request.json["name"]
    email = request.json["email"]
    
    return jsonify({"success": "Successful Post"})


@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Execute a simple query to check the connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Database connection successful'})
    except Exception as e:
        app.logger.error(f"Database connection failed: {str(e)}")
        return jsonify({'message': 'Database connection failed', 'error': str(e)})

if __name__ == '__main__':
    app.debug = True
    app.run()