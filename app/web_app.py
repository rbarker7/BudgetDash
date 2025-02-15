from flask import Flask, Blueprint, render_template, redirect
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from pathlib import Path

class WebApp:
    """Base class to initialize Flask with blueprint registration."""
    
    def __init__(self):
        # Initialize Flask
        project_root = Path(__file__).resolve().parent.parent
        template_dir = project_root / "templates"

        # Check that templates/ exists
        if not template_dir.exists():
            return f"Error: Template file not found at {template_dir.resolve()}", 500
        
        # Initialize Flask server
        self.server = Flask(__name__, template_folder=str(template_dir))

        # Initialize Blueprint and register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register Flask routes directly in WebApp."""
        main_bp = Blueprint('main', __name__)

        @main_bp.route("/")
        def home(): 
            return render_template("index.html")

        @main_bp.route("/dashboard")
        def dashboard_redirect():
            return redirect("/dashboard/")

        self.server.register_blueprint(main_bp)
    
    def run(self, debug, host, port):
        """Run the Flask server with configurable parameters."""
        self.server.run(debug=debug, host=host, port=port)

class DashApp(WebApp):
    """Dash app that extends WebApp."""

    def __init__(self):
        # Initialize Flask (via parent class)
        super().__init__()

        # Initialize Dash within Flask
        self.app = dash.Dash(
            __name__,
            server=self.server,
            url_base_pathname='/dashboard/',
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

        # Set up the layout
        self._set_layout()

    def _set_layout(self):
        """Define the Dash layout."""
        sidebar = dbc.Nav(
            [
                dbc.NavLink("Net Worth", href="#", active="exact"),
                dbc.NavLink("Budget", href="#", active="exact"),
                dbc.NavLink("Investments", href="#", active="exact"),
                dbc.NavLink("Cash Flow", href="#", active="exact"),
            ],
            vertical=True,
            pills=True,
        )

        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Budget Dashboard"), width=12)
            ]),
            dbc.Row([
                dbc.Col(sidebar, width=3),
                dbc.Col(html.Div("Main Content Area"), width=9)
            ])
        ], fluid=True)
