import uuid
import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    priority: int = 3
    sub_tasks: List['Task'] = Field(default_factory=list)
    completed: bool = False


Task.model_rebuild()
