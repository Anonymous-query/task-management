from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from ..models.task import Task
from ..models.user import User, UserRole
from ..schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def get_task(self, db: Session, task_id: int, current_user: User) -> Optional[Task]:
        query = db.query(Task).filter(Task.id == task_id)
        
        # If user is not admin, only allow access to their own tasks
        if current_user.role != UserRole.ADMIN:
            query = query.filter(Task.created_by == current_user.id)
        
        return query.first()
    
    def get_tasks(
        self, 
        db: Session, 
        current_user: User,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        query = db.query(Task)
        
        # If user is not admin, only show their own tasks
        if current_user.role != UserRole.ADMIN:
            query = query.filter(Task.created_by == current_user.id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_task(self, db: Session, task: TaskCreate, current_user: User) -> Task:
        db_task = Task(
            **task.model_dump(),
            created_by=current_user.id
        )
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    def update_task(
        self, 
        db: Session, 
        task_id: int, 
        task_update: TaskUpdate,
        current_user: User
    ) -> Optional[Task]:
        db_task = self.get_task(db, task_id, current_user)
        if not db_task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    
    def delete_task(self, db: Session, task_id: int, current_user: User) -> bool:
        db_task = self.get_task(db, task_id, current_user)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True
    
    def get_user_tasks(
        self, 
        db: Session, 
        user_id: int, 
        current_user: User,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        # Only admins can view other users' tasks
        if current_user.role != UserRole.ADMIN and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view these tasks"
            )
        
        return db.query(Task).filter(
            Task.created_by == user_id
        ).offset(skip).limit(limit).all()


task_service = TaskService()