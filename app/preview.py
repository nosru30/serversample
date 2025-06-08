import os
from .db import SessionLocal, RoleORM, UserORM, EmployeeORM, DepartmentORM
from . import auth


def load_preview_data() -> None:
    """Seed the database with demo records when PREVIEW_MODE=1."""
    if os.getenv("PREVIEW_MODE") != "1":
        return

    session = SessionLocal()
    try:
        # Skip seeding if any users already exist
        if session.query(UserORM).first():
            return

        # Roles
        role_emp = RoleORM(name="employee")
        role_admin = RoleORM(name="admin")
        session.add_all([role_emp, role_admin])
        session.commit()

        # Department
        dept = DepartmentORM(name="General")
        session.add(dept)
        session.commit()

        # Demo user and employee
        user = UserORM(
            email="demo@example.com",
            password=auth.hash_password("demo"),
            role_id=role_emp.id,
        )
        session.add(user)
        session.commit()

        emp = EmployeeORM(
            user_id=user.id,
            employee_id="E001",
            name="Demo User",
            department_id=dept.id,
        )
        session.add(emp)
        session.commit()
    finally:
        session.close()

