# app/__init__.py
from flask import Flask
from flask_session import Session
from .config import Config
import os

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
    app.config.from_object(Config)
    
    # Initialize Flask-Session
    Session(app)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app