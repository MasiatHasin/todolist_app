from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todolists = relationship("ToDoList", back_populates="owner")

class ToDoList(Base):
    __tablename__ = "todolists"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, default=0)
    tag = Column(String, default="untagged")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todolists")
    tasks = relationship("Task", back_populates="todolist", cascade="all, delete")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task = Column(String, index=True)
    priority = Column(Integer, default=0)
    is_done = Column(Boolean, default = False)
    todolist_id = Column(Integer, ForeignKey("todolists.id"))

    todolist = relationship("ToDoList", back_populates="tasks")