from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import text,inspect
import os
from pathlib import Path
import logging
from .models.models import db, Users

# Load environment variables from .env file
load_dotenv(dotenv_path=Path('.') / '.env', override=True)
app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"connection url:\t{app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize the database with the app
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_or_update_tables():
    try:
        inspector = inspect(db.engine)
        db.create_all()
        logger.info('Tables created successfully')

        for table_name in db.metadata.tables.keys():
            if inspector.has_table(table_name):
                columns_in_db = {column['name'] for column in inspector.get_columns(table_name)}
                model_columns = {column.name for column in db.metadata.tables[table_name].columns}
                new_columns = model_columns - columns_in_db

                for column in new_columns:
                    column_obj = db.metadata.tables[table_name].columns[column]
                    db.engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_obj.compile(dialect=db.engine.dialect)}')
                logger.info(f'Table {table_name} updated successfully')
    except Exception as e:
        logger.error(f'Error creating/updating tables: {str(e)}')



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

@app.route('/check_tables', methods=['GET'])
def check_tables():
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if tables:
            return jsonify({'message': 'Tables exist', 'tables': tables})
        else:
            return jsonify({'message': 'No tables found'})
    except Exception as e:
        return jsonify({'message': 'Failed to check tables', 'error': str(e)})

if __name__ == '__main__':
    with app.app_context():
        create_or_update_tables()
    app.debug = True
    app.run()