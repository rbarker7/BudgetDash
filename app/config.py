import configparser
import os

# Get absolute path to config file
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.ini')

def load_config():
    """Loads configuration settings from config.ini."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config
