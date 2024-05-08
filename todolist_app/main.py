from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

from typing import List

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/todolists/", response_model=schemas.ToDoList)
def create_todolist_for_user(
    user_id: int, todolist: schemas.ToDoListCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todolist(db=db, todolist=todolist, user_id=user_id)

@app.get("/users/{user_id}/todolists/", response_model=List[schemas.ToDoListShort])
def get_todolist_for_user(user_id: int, db: Session = Depends(get_db)):
    todolists = crud.get_user_todolists(db=db, user_id=user_id)
    if todolists is None:
        raise HTTPException(status_code=404, detail="No todolists found")
    return todolists

@app.get("/users/{user_id}/todolists/{todolist_id}/", response_model=schemas.ToDoListLong)
def read_todolist(todolist_id: int, db: Session = Depends(get_db)):
    todolist = crud.get_todolist(db, todolist_id = todolist_id)
    if todolist is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return todolist

@app.patch("/users/{user_id}/todolists/{todolist_id}/", response_model=schemas.ToDoList)
def update_todolist(todolist_id: str, todolist: schemas.ToDoListUpdate, db: Session = Depends(get_db)):
    stored_todolist_data = crud.get_todolist(db, todolist_id = todolist_id)
    if stored_todolist_data:
        update_data = todolist.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_todolist_data, key, value)
        db.commit()
        stored_todolist_data = crud.get_todolist(db, todolist_id = todolist_id)
        return stored_todolist_data
    raise HTTPException(status_code=404, detail="ToDoList not found")

@app.delete("/users/{user_id}/todolists/{todolist_id}/", response_model=schemas.ToDoListDeleted)
def delete_todolist(todolist_id: int, db: Session = Depends(get_db)):
    todolist = crud.delete_todolist(db, todolist_id = todolist_id)
    if todolist is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return todolist

@app.post("/users/{user_id}/todolists/{todolist_id}/tasks/", response_model=schemas.Task)
def create_task_for_user(
    todolist_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_task(db=db, task=task, todolist_id=todolist_id)

@app.get("/users/{user_id}/todolists/{todolist_id}/tasks/{task_id}/", response_model=schemas.TaskShort)
def get_task(task_id: int, todolist_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id, todolist_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/users/{user_id}/todolists/{todolist_id}/tasks/{task_id}/", response_model=schemas.Task)
def update_task(task_id: str, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    stored_task_data = crud.get_task(db, task_id = task_id)
    if stored_task_data:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_task_data, key, value)
        db.commit()
        db.refresh(stored_task_data)
        stored_task_data = crud.get_task(db, task_id = task_id)
        return stored_task_data
    raise HTTPException(status_code=404, detail="ToDoList not found")