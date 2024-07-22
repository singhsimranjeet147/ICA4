from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='static')
CORS(app)
load_dotenv()

# Function to establish database connection
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST')
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

# Route to handle POST requests for uploading data
@app.route('/', methods=['POST'])
def upload_to_database():
    # Get data from request form
    name = request.form.get('name')
    address = request.form.get('address')

    # Validate data (ensure name and address are not None or empty)
    if not name or not address:
        return jsonify({'error': 'Name and address are required fields'}), 400

    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    
    # Use context manager for cursor and commit transaction
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO info (name, address) VALUES (%s, %s)", (name, address))
            conn.commit()
            return jsonify({'message': 'Data uploaded successfully'}), 200
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({'error': 'Failed to upload data to database. Please try again', 'details': str(e)}), 500
        finally:
            conn.close()  # Close connection explicitly (though should be closed by context manager)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
