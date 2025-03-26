from flask import Flask, request, jsonify  # Import Flask and necessary modules
import os  # For handling file paths
from werkzeug.utils import secure_filename  # To securely handle file uploads
from .firestore_db import add_data_to_firestore  # Import Firestore function
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import time
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load the trained model
MODEL_PATH = "TrainedModelRecyclable.keras"
model = load_model(MODEL_PATH)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img = Image.open(BytesIO(file.read()))  # Open image from the file object in memory

    # Resize image and preprocess it for the model
    img = img.resize((224, 224))  # Resize to model's input size
    img_array = image.img_to_array(img) / 255.0  # Convert image to array and normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model.predict(img_array)
    predicted_class = int(predictions[0][0] > 0.5)  # Assuming binary classification

    labels = ["Non-Recyclable", "Recyclable"]
    result = labels[predicted_class]

    
    # Prepare data to add to Firestore
    data = {
        "prediction": result,
        "image_name": secure_filename(file.filename),  # You can save the image name as well
    }

    # Add the prediction data to Firestore
    doc_id = add_data_to_firestore(data)

    return jsonify({"prediction": result})


@app.route('/')
def home():
    """Default route to check if the API is running"""
    return "Flask API is running!"


@app.route("/add-data", methods=["POST"])
def add_data():
    """Handles adding JSON data to Firestore"""
    data = request.json  # Get data from request body
    doc_id = add_data_to_firestore(data)  # Call function from firestore_service.py
    
    return jsonify({"message": "Data added successfully", "id": doc_id})  # Return success response with document ID


if __name__ == "__main__":
    app.run(debug=True)  # Only ONE instance of app.run()
