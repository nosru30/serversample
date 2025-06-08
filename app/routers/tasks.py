from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Task
import logging
from ..db import SessionLocal, engine, TaskORM
from ..migrate import run_migrations

logger = logging.getLogger(__name__)

# Ensure tables exist and log the outcome so startup issues are visible
logger.info("Ensuring database tables exist")
run_migrations()
logger.info("Database tables ready")

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _create_task_recursive(task: Task, db: Session, parent_id: Optional[str] = None) -> Task:
    task_orm = TaskORM(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        completed=task.completed,
        parent_id=parent_id,
    )
    db.add(task_orm)
    db.commit()
    db.refresh(task_orm)
    sub_tasks = [
        _create_task_recursive(st, db, parent_id=task_orm.id)
        for st in task.sub_tasks
    ]
    return Task(
        id=UUID(task_orm.id),
        title=task_orm.title,
        description=task_orm.description,
        due_date=task_orm.due_date,
        priority=task_orm.priority,
        completed=task_orm.completed,
        sub_tasks=sub_tasks,
    )


def _build_task_recursive(task_orm: TaskORM, db: Session) -> Task:
    children = (
        db.query(TaskORM).filter(TaskORM.parent_id == task_orm.id).all()
    )
    sub_tasks = [_build_task_recursive(ch, db) for ch in children]
    return Task(
        id=UUID(task_orm.id),
        title=task_orm.title,
        description=task_orm.description,
        due_date=task_orm.due_date,
        priority=task_orm.priority,
        completed=task_orm.completed,
        sub_tasks=sub_tasks,
    )


def _delete_sub_tasks(task_orm: TaskORM, db: Session) -> None:
    children = db.query(TaskORM).filter(TaskORM.parent_id == task_orm.id).all()
    for ch in children:
        _delete_sub_tasks(ch, db)
        db.delete(ch)


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task, db: Session = Depends(get_db)):
    return _create_task_recursive(task, db)


@router.get("/", response_model=List[Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskORM).filter(TaskORM.parent_id == None).all()
    return [_build_task_recursive(t, db) for t in tasks]


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return _build_task_recursive(task, db)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description
    task.due_date = task_update.due_date
    task.priority = task_update.priority
    task.completed = task_update.completed
    _delete_sub_tasks(task, db)
    db.commit()
    for st in task_update.sub_tasks:
        _create_task_recursive(st, db, parent_id=task.id)
    db.commit()
    db.refresh(task)

    return _build_task_recursive(task, db)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    _delete_sub_tasks(task, db)
    db.delete(task)
    db.commit()
    return
