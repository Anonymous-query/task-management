from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskWithUser
from ...services.task_service import task_service
from ...models.user import User
from ..deps import get_current_active_user

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task"""
    return task_service.create_task(db=db, task=task, current_user=current_user)


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks (user sees only their tasks, admin sees all)"""
    return task_service.get_tasks(db, current_user, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get task by ID"""
    task = task_service.get_task(db, task_id=task_id, current_user=current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update task by ID"""
    updated_task = task_service.update_task(db, task_id, task_update, current_user)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete task by ID"""
    if not task_service.delete_task(db, task_id, current_user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

@router.get("/user/{user_id}", response_model=List[TaskResponse])
def read_user_tasks(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks for a specific user (admin can see any user, users can see only their own)"""
    return task_service.get_user_tasks(db, user_id, current_user, skip=skip, limit=limit)