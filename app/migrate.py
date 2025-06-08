import logging
from app.db import Base, engine

# Configure basic logging so migration status is visible when the script runs.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Running migrations")
    logger.info("Using database URL: %s", engine.url)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Migrations completed successfully")
    except Exception:
        logger.exception("Migration failed")
        raise
