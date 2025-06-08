import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from .db import Base

class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=3)
    completed = Column(Boolean, default=False)
