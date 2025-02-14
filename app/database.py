from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import app.models as models
from app.logger import logger
from app.config import db_path 

class Database:
    """
    A class to handle database initialization and session management.

    This class:
    - Ensures the database directory exists.
    - Initializes the database engine upon creation.
    - Provides a session factory for handling database transactions.
    """

    def __init__(self):
        """Initialize the database connection and session factory."""
        self._engine = None
        self._SessionLocal = None
        try:
            self._initialize_db()
            self._check_db_file()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}", exc_info=True)
            raise

    def _initialize_db(self):
        """
        Ensures the database directory exists and sets up the database engine.

        This method:
        - Creates the parent directory for the database file if it does not exist.
        - Initializes the SQLite database engine.
        - Creates a session factory for database interactions.
        """
        logger.info(f"Initializing database at: {db_path}")

        try:
            # Ensure the parent directory exists
            db_path.parent.mkdir(parents=True, exist_ok=True)

            # Create the database engine
            self._engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

            # Create a session factory
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

            logger.info("Database engine and session created successfully.")

        except Exception as e:
            logger.error(f"Failed to initialize the database: {e}", exc_info=True)
            raise

    def _check_db_file(self):
        """
        Ensures the SQLite database file exists. If it does not exist, logs a warning.
        """
        if not db_path.exists():
            logger.warning(f"Database file {db_path} does not exist yet. It will be created when tables are added.")

    def get_db_session(self):
        """
        Provides a new database session to be used in a `with` context.

        This function:
        - Yields a session object for performing database operations.
        - Ensures the session is properly closed after use.

        Yields:
            Session: A SQLAlchemy session object.
        """
        db = None
        try:
            db = self._SessionLocal()
            logger.debug("Database session created.")
            yield db
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            if db:
                db.close()
                logger.debug("Database session closed.")

    def create_tables(self):
        """
        Ensures all database tables are created.
        This should be called once at startup to set up the schema.
        """
        try:
            models.Base.metadata.create_all(bind=self._engine)
            logger.info("All tables have been created successfully.")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}", exc_info=True)
            raise

