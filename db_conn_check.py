from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
from .app import db

db_conn_check_bp = Blueprint('db_conn_check', __name__)


@db_conn_check_bp.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Execute a simple query to check the connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Database connection successful'})
    except Exception as e:
        # app.logger.error(f"Database connection failed: {str(e)}")
        return jsonify({'message': 'Database connection failed', 'error': str(e)})

@db_conn_check_bp.route('/check_tables', methods=['GET'])
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