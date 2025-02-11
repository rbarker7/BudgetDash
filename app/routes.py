from flask import render_template
from pathlib import Path

def register_routes(app):
    @app.route("/")
    def home():
        template_file = Path("templates") / "index.html"
        
        if not template_file.exists():
            return f"Error: Template file not found at {template_file.resolve()}", 500

        return render_template("index.html")
