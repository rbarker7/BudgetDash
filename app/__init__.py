from flask import Flask
from pathlib import Path
from .database import Database

def create_app():
    """Create and configure the Flask app."""
    project_root = Path(__file__).resolve().parent.parent  # Get project root
    template_dir = project_root / "templates"  # Use Path for templates directory

    print(f"Using template directory: {template_dir}")  # Debugging line

    app = Flask(__name__, template_folder=str(template_dir))

    from app.routes import register_routes
    register_routes(app)

    return app
