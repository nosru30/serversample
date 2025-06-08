from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Task
from ..db import SessionLocal, Base, engine
from ..db_models import TaskORM

# Ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/dbtasks", tags=["dbtasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task, db: Session = Depends(get_db)):
    task_orm = TaskORM(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        completed=task.completed,
    )
    db.add(task_orm)
    db.commit()
    db.refresh(task_orm)
    return Task(
        id=UUID(task_orm.id),
        title=task_orm.title,
        description=task_orm.description,
        due_date=task_orm.due_date,
        priority=task_orm.priority,
        completed=task_orm.completed,
        sub_tasks=[],
    )


@router.get("/", response_model=List[Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskORM).all()
    return [
        Task(
            id=UUID(t.id),
            title=t.title,
            description=t.description,
            due_date=t.due_date,
            priority=t.priority,
            completed=t.completed,
            sub_tasks=[],
        )
        for t in tasks
    ]


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(
        id=UUID(task.id),
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        completed=task.completed,
        sub_tasks=[],
    )


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
    db.commit()
    db.refresh(task)

    return Task(
        id=UUID(task.id),
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        completed=task.completed,
        sub_tasks=[],
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return
