from pydantic import BaseModel
from typing import Optional

# Task
class TaskBase(BaseModel):
    task: str
    priority: int | None = None

class TaskCreate(TaskBase):
    pass

class TaskShort(TaskBase):
    is_done: bool
    id: int

    class Config:
        orm_mode = True

class Task(TaskShort):
    todolist_id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    task : str | None = None
    priority: int | None = None

# ToDoList
class ToDoListBase(BaseModel):
    title : str
    description: str
    priority: int | None = None
    tag: str | None = None

class ToDoListCreate(ToDoListBase):
    pass

class ToDoList(ToDoListBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ToDoListShort(BaseModel):
    id: int
    title : str
    description: str

class ToDoListLong(ToDoList):
    tasks : list[TaskShort] = []

class ToDoListUpdate(BaseModel):
    title : str | None = None
    description: str | None = None
    priority: int | None = None
    tag: str | None = None

class ToDoListDeleted(BaseModel):
    id: int
    title: str

# User
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool