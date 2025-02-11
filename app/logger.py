import logging
from pathlib import Path
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Generate timestamped log filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = LOG_DIR / f"log_{timestamp}.log"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Logs to a timestamped file
        logging.StreamHandler()  # Also log to terminal
    ]
)

logger = logging.getLogger(__name__)
