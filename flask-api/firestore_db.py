import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")  # Load Firebase credentials
firebase_admin.initialize_app(cred)  # Initialize Firebase app
db = firestore.client()  # Initialize Firestore AFTER Firebase is initialized

def add_data_to_firestore(data):
    """Saves prediction data to Firestore with an auto-generated document ID and timestamp"""
    data["timestamp"] = firestore.SERVER_TIMESTAMP  # Add Firestore server timestamp
    doc_ref = db.collection("test_collection").add(data)  # Save data in Firestore

    return doc_ref[1].id  # Correctly return the document ID
