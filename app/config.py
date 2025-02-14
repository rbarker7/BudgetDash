import configparser
from pathlib import Path

# Get absolute path to config.ini
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.ini"

def load_config():
    """Loads configuration settings from config.ini."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config

# Load the config
config = load_config()

# Resolve the database path but don't create directories here
db_path = Path(config["database"]["db_path"]).expanduser()
