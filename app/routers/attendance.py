import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from ..db import (
    SessionLocal,
    UserORM,
    EmployeeORM,
    AttendanceORM,
    RoleORM,
)
from .. import auth
from ..schemas import (
    UserCreate,
    LoginResponse,
    UserRead,
    AttendanceCreate,
    AttendanceRead,
)

router = APIRouter(tags=["attendance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_token(auth_header: str = Header(..., alias="Authorization")) -> str:
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    return auth_header.split(" ", 1)[1]


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(_get_token)
) -> UserORM:
    user_id = auth.get_user_id(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(UserORM).filter(UserORM.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_employee(
    current_user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EmployeeORM:
    employee = (
        db.query(EmployeeORM).filter(EmployeeORM.user_id == current_user.id).first()
    )
    if not employee:
        raise HTTPException(status_code=400, detail="Employee record not found")
    return employee


@router.post("/login", response_model=LoginResponse)
def login(credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserORM).filter(UserORM.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_token(user.id)
    return LoginResponse(token=token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    role = db.query(RoleORM).filter(RoleORM.id == current_user.role_id).first()
    if not role:
        raise HTTPException(status_code=500, detail="Role not found")
    role_name = role.name
    return UserRead(id=current_user.id, email=current_user.email, role=role_name)


@router.post("/attendances", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
def create_attendance(
    attendance: AttendanceCreate,
    current_employee: EmployeeORM = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    att = AttendanceORM(
        employee_id=current_employee.id,
        date=attendance.date,
        start_time=attendance.start_time,
        end_time=attendance.end_time,
        break_duration_minutes=attendance.break_duration_minutes,
        notes_free_text=attendance.notes_free_text,
    )
    db.add(att)
    db.commit()
    db.refresh(att)
    return AttendanceRead.model_validate(att)


@router.get("/attendances", response_model=List[AttendanceRead])
def read_my_attendances(
    month: Optional[str] = None,
    current_employee: EmployeeORM = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    query = db.query(AttendanceORM).filter(
        AttendanceORM.employee_id == current_employee.id
    )
    if month:
        try:
            year, mon = map(int, month.split("-"))
            start = datetime.date(year, mon, 1)
            if mon == 12:
                end = datetime.date(year + 1, 1, 1)
            else:
                end = datetime.date(year, mon + 1, 1)
            query = query.filter(AttendanceORM.date >= start, AttendanceORM.date < end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid month format")
    records = query.all()
    return [AttendanceRead.model_validate(r) for r in records]


@router.delete("/attendances/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    current_employee: EmployeeORM = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    record = db.query(AttendanceORM).filter(
        AttendanceORM.id == attendance_id,
        AttendanceORM.employee_id == current_employee.id,
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(record)
    db.commit()
    return
