import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")  # Load Firebase credentials
firebase_admin.initialize_app(cred)  # Initialize Firebase app
db = firestore.client()  # Initialize Firestore AFTER Firebase is initialized

def add_data_to_firestore(data):
    """Adds data to Firestore and returns the document ID."""
    doc_ref = db.collection("test_collection").document()  # Create new Firestore document
    doc_ref.set(data)  # Save data to Firestore
    return doc_ref.id  # Return the document ID
