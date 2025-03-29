import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")  # Load Firebase credentials
firebase_admin.initialize_app(cred)  # Initialize Firebase app
db = firestore.client()  # Initialize Firestore AFTER Firebase is initialized

def add_data_to_firestore(data):
    """Saves prediction data to Firestore with an auto-generated document ID"""
    data["timestamp"] = firestore.SERVER_TIMESTAMP  # Add timestamp
    doc_ref = db.collection("predictions").add(data)  # Firestore auto-generates ID
    return doc_ref.id  # Return the document ID
