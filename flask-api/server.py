from flask import Flask, request, jsonify  # Import Flask and necessary modules
import os  # For handling file paths
from werkzeug.utils import secure_filename  # To securely handle file uploads
from firestore_db import add_data_to_firestore  # Import Firestore function

app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set the upload folder in Flask config

@app.route('/')
def home():
    """Default route to check if the API is running"""
    return "Flask API is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file upload to the server"""
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400  # Return error if no file is uploaded
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400  # Return error if no file is selected

    filename = secure_filename(file.filename)  # Secure the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Define file path
    file.save(file_path)  # Save the file

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200  # Return success response

@app.route('/add-data', methods=['POST'])
def add_data():
    """Handles adding JSON data to Firestore"""
    data = request.json  # Get data from request body
    doc_id = add_data_to_firestore(data)  # Call function from firestore_service.py
    
    return jsonify({"message": "Data added successfully", "id": doc_id})  # Return success response with document ID

if __name__ == '__main__':
    # Run the app in debug mode (for development only)
    # TODO: When deploying, remove debug=True and set up a production WSGI server
    app.run(debug=True)
