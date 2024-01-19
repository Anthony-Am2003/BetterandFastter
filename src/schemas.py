# schemas.py

from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class TaskBase(BaseModel):
    description: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
