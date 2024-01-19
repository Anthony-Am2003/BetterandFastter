from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: int
    name: str
    email: str

users_db = []

@app.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found")

class Task(BaseModel):
    id: int
    title: str
    description: str
    complete: bool

tasks_db = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def complete_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            task.complete = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            deleted_task = tasks_db.pop(i)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")