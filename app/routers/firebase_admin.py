import firebase_admin
from firebase_admin import auth

# Initialize Firebase Admin using the default credentials from the environment variable
firebase_admin.initialize_app()

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {e}")
        return None
