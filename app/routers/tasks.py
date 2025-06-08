from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.models import Task  # Assuming models.py is in the app directory

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

tasks_db: List[Task] = []


# Helper function to find a task recursively
def _find_task_recursive(task_id: UUID,
                         task_list: List[Task]) -> Optional[Task]:
    for task in task_list:
        if task.id == task_id:
            return task
        if task.sub_tasks:
            found_in_sub = _find_task_recursive(task_id, task.sub_tasks)
            if found_in_sub:
                return found_in_sub
    return None


# Helper function to delete a task recursively
def _delete_task_recursive(task_id: UUID, task_list: List[Task]) -> bool:
    for i, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(i)
            return True
        if task.sub_tasks:
            if _delete_task_recursive(task_id, task.sub_tasks):
                return True
    return False


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    # The Task model already assigns a UUID if not provided.
    # It also handles default for sub_tasks.
    # We need to ensure any provided sub_tasks also get IDs if they don't
    # have them. This is complex if sub_tasks can have their own sub_tasks
    # deeply nested. For now, Pydantic handles the creation of sub_task models.
    tasks_db.append(task)
    return task


@router.get("/", response_model=List[Task])
async def read_tasks():
    return tasks_db


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: UUID):
    task = _find_task_recursive(task_id, tasks_db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_update: Task):
    task = _find_task_recursive(task_id, tasks_db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")

    # Update fields, ensuring ID from path is respected
    task.title = task_update.title
    task.description = task_update.description
    task.due_date = task_update.due_date
    task.priority = task_update.priority
    task.completed = task_update.completed
    task.sub_tasks = task_update.sub_tasks  # Direct replacement for now

    # The ID of the task itself should not change to task_update.id
    # task.id remains task_id from the path

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID):
    deleted = _delete_task_recursive(task_id, tasks_db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    return  # No content
