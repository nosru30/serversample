import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
import uuid

# Read the connection string from the standard DATABASE_URL environment
# variable. Tests will set this to a temporary SQLite database when a real
# database isn't available.
# Allow forcing SQLite with an env flag (useful for offline dev/CI)
FORCE_SQLITE = os.getenv("FORCE_SQLITE", "false").lower() == "true"

# Prefer DATABASE_URL when supplied, otherwise fall back to local SQLite.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or FORCE_SQLITE:
    DATABASE_URL = "sqlite:///./local.db"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=3)
    completed = Column(Boolean, default=False)
    parent_id = Column(String(36), ForeignKey("tasks.id"), nullable=True)
