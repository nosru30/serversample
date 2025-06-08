import datetime
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str

class UserRead(BaseModel):
    id: int
    email: str
    role: str

class AttendanceCreate(BaseModel):
    date: datetime.date
    start_time: datetime.datetime
    end_time: datetime.datetime
    break_duration_minutes: int = 0
    notes_free_text: Optional[str] = None

class AttendanceRead(AttendanceCreate):
    id: int
    employee_id: int
