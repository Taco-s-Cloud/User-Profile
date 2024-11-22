#User-profile/app/init.py
from flask import Flask
from flask_cors import CORS
from .routers import user_blueprint
from .database import engine, Base

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register user blueprint
    app.register_blueprint(user_blueprint)

    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)

    return app
