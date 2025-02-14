import time
from app import create_app
from app.config import load_config
from app.logger import logger
from app import Database

# Start timing
start_time = time.time()

# Load config
config = load_config()

# Initialize the database before anything else
db = Database()
db.create_tables()

# Create Flask app
app = create_app()

if __name__ == "__main__":
    debug_mode = config.getboolean("flask", "debug")
    host = config.get("flask", "host")
    port = config.getint("flask", "port")

    logger.info("Starting the Budget Dashboard...")

    try:
        app.run(debug=debug_mode, host=host, port=port)
    except Exception as e:
        logger.error(f"Error starting the app: {e}")

    startup_time = time.time() - start_time
    logger.info(f"App started in {startup_time:.2f} seconds")
