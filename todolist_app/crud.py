from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_todolist(db: Session, todolist: schemas.ToDoListCreate, user_id: int):
    db_todolist= models.ToDoList(**todolist.model_dump(), owner_id=user_id)
    db.add(db_todolist)
    db.commit()
    db.refresh(db_todolist)
    return db_todolist

def get_user_todolists(db: Session, user_id: int):
    return db.query(models.ToDoList).filter(models.ToDoList.owner_id == user_id).all()

def get_todolist(db: Session, todolist_id: int):
    return db.query(models.ToDoList).filter(models.ToDoList.id == todolist_id).first()

def delete_todolist(db: Session, todolist_id: int):
    todolist = get_todolist(db, todolist_id)
    db.delete(todolist)
    db.commit()
    return todolist

def create_task(db: Session, task: schemas.TaskCreate, todolist_id: int):
    db_task= models.Task(**task.model_dump(), todolist_id = todolist_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int, todolist_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.todolist_id == todolist_id).first()