# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import List
from .schemas import UserBase, UserCreate, User, TaskBase, TaskCreate, Task

app = FastAPI()

# Middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect to /docs automatically
@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

# Users database
users_db = []

@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    user_data = user.dict()
    user_data["id"] = len(users_db) + 1
    new_user = User(**user_data)
    users_db.append(new_user)
    return new_user

@app.get("/users/", response_model=List[User])
def read_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Tasks database
tasks_db = []

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    task_data = task.dict()
    task_data["id"] = len(tasks_db) + 1
    new_task = Task(**task_data)
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            deleted_task = tasks_db.pop(i)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")
