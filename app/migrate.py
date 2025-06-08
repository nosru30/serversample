import logging

from .db import Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migrations() -> None:
    """Drop all tables and recreate them to match current models."""
    logger.info("Dropping existing tables")
    Base.metadata.drop_all(bind=engine)
    logger.info("Creating database tables")
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    try:
        run_migrations()
        logger.info("Migrations completed successfully")
    except Exception:
        logger.exception("Migration failed")
        raise
