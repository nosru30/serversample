import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

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

    @staticmethod
    def _ensure_utc(value: datetime.datetime) -> datetime.datetime:
        if value.tzinfo is None:
            # Assume naive datetimes are already in UTC
            return value.replace(tzinfo=datetime.timezone.utc)
        if value.tzinfo != datetime.timezone.utc:
            raise ValueError("Datetime must be timezone-aware UTC")
        return value

    _normalize_start_time = field_validator("start_time")(_ensure_utc)
    _normalize_end_time = field_validator("end_time")(_ensure_utc)

class AttendanceRead(AttendanceCreate):
    id: int
    employee_id: int
    model_config = {"from_attributes": True}
