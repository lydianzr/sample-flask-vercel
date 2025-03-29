from flask import Flask, request, jsonify  # Import Flask and necessary modules
import os  # For handling file paths
from werkzeug.utils import secure_filename  # To securely handle file uploads
from .firestore_db import add_data_to_firestore  # Import Firestore function
import tensorflow as tf
import numpy as np
import time
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load the trained model
TFLITE_MODEL_PATH = "TrainedModelRecyclable.tflite"

# Load TFLite model into an interpreter
interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img = Image.open(BytesIO(file.read()))  # Open image from the file object in memory

    # Resize image and preprocess it for the model
    img = img.resize((224, 224))  # Resize to model's input size
    img_array = np.array(img, dtype=np.float32) / 255.0  # Convert image to NumPy array and normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    interpreter.set_tensor(input_details[0]["index"], img_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]["index"])

    # Assuming binary classification (0 = Non-Recyclable, 1 = Recyclable)
    predicted_class = int(predictions[0][0] > 0.5)
    labels = ["Non-Recyclable", "Recyclable"]
    result = labels[predicted_class]

    # Save to Firestore
    data = {
        "prediction": result,
        "image_name": secure_filename(file.filename),
    }
    doc_id = add_data_to_firestore(data)

    return jsonify({"prediction": result, "doc_id": doc_id})



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
