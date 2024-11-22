#app/routers/user.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_profile import User
from datetime import datetime
import bcrypt

user_blueprint = Blueprint("users", __name__)

@user_blueprint.route("/api/register", methods=["POST"])
def register_user():
    data = request.json
    db: Session = next(get_db())

    # Log the incoming data for debugging
    print("Register endpoint hit. Incoming data:", data)

    try:
        # Check if the user already exists by email
        existing_user = db.query(User).filter(User.email == data["email"]).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 400

        # Check if the username already exists
        existing_username = db.query(User).filter(User.username == data["username"]).first()
        if existing_username:
            return jsonify({"error": "Username already exists"}), 400

        # Hash password for security
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Create a new user
        new_user = User(
            first_name=data.get("firstName", "Unknown"),
            last_name=data.get("lastName", "Unknown"),
            username=data["username"],
            email=data["email"],
            password=hashed_password.decode('utf-8'),
            registration_date=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()

        # Confirm the user has been added
        print(f"User {new_user.username} registered successfully!")
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        # Log the error for debugging
        print("Error in registration:", str(e))
        return jsonify({"error": "An error occurred during registration"}), 500


@user_blueprint.route("/api/login", methods=["POST"])
def login_user():
    data = request.json
    db: Session = next(get_db())

    # Log the incoming login request
    print("Login endpoint hit. Incoming data:", data)

    try:
        # Find the user by email or username
        user = db.query(User).filter(
            (User.email == data["email"]) | (User.username == data["email"])
        ).first()

        if user and bcrypt.checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
            print(f"User {user.username} logged in successfully!")
            return jsonify({"message": "Login successful!"}), 200
        else:
            print("Invalid login attempt")
            return jsonify({"error": "Invalid email/username or password"}), 401

    except Exception as e:
        # Log the error for debugging
        print("Error in login:", str(e))
        return jsonify({"error": "An error occurred during login"}), 500
