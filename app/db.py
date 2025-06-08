import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Date,
    UniqueConstraint,
)
import uuid

# Read the connection string from the standard DATABASE_URL environment
# variable. Tests will set this to a temporary SQLite database when a real
# database isn't available.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set")

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


class RoleORM(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


class DepartmentORM(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class EmployeeORM(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    employee_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)


class NoteMasterORM(Base):
    __tablename__ = "note_master"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class AttendanceORM(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    break_duration_minutes = Column(Integer, default=0, nullable=False)
    notes_free_text = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="uix_employee_date"),
    )


class AttendanceNoteORM(Base):
    __tablename__ = "attendance_notes"

    attendance_id = Column(Integer, ForeignKey("attendances.id"), primary_key=True)
    note_master_id = Column(Integer, ForeignKey("note_master.id"), primary_key=True)
