import logging
import os
from pathlib import Path
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent


def run_migrations():
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BASE_DIR / "alembic"))
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(cfg, "head")


if __name__ == "__main__":
    logger.info("Running Alembic migrations")
    try:
        run_migrations()
        logger.info("Migrations completed successfully")
    except Exception:
        logger.exception("Migration failed")
        raise
