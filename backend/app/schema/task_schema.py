from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, validator

from app.model.base_model import Category


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False
    due_date: Optional[datetime] = None
    category: Optional[Category] = Category.LOW
    completed_at: Optional[datetime] = None
    
    


class TaskCreate(TaskBase):
    owner_id: int
    
    @validator('due_date', pre=True, always=True)
    def parse_and_validate_due_date(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError('Invalid datetime format. Must be ISO 8601 format.')

        if isinstance(value, datetime) and value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)

        if value and value <= datetime.now().replace(tzinfo=None):
            raise ValueError('Due date must be greater than the current date')

        return value


class TaskUpdate(TaskBase):
    owner_id: int
    
    @validator('due_date', pre=True, always=True)
    def parse_and_validate_due_date(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError('Invalid datetime format. Must be ISO 8601 format.')

        if isinstance(value, datetime) and value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)

        if value and value <= datetime.now().replace(tzinfo=None):
            raise ValueError('Due date must be greater than the current date')

        return value


class TaskInDB(TaskBase):
    id: int
    delete_request: Optional[bool]
    owner_id: Optional[int]
    status: Optional[bool]


class TaskList(BaseModel):
    tasks: List[TaskInDB]
    total: int
    skip: int
    limit: int


class Message(BaseModel):
    message: str