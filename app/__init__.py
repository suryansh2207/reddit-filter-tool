from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.secret_key = "sudo2207"  # Ensure your secret key is set

    # Import and initialize routes
    from .routes import init_app
    init_app(app)

    return app

