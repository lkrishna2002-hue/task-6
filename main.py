# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import Base, engine, get_db

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo CRUD API",
    description="Simple CRUD API for managing todo items.",
    version="1.0.0"
)


@app.get("/health", tags=["health"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}


@app.post(
    "/todos",
    response_model=schemas.Todo,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"]
)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db)
):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get(
    "/todos",
    response_model=List[schemas.Todo],
    tags=["todos"]
)
def list_todos(
    db: Session = Depends(get_db)
):
    todos = db.query(models.Todo).all()
    return todos


@app.get(
    "/todos/{todo_id}",
    response_model=schemas.Todo,
    tags=["todos"]
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return todo


@app.put(
    "/todos/{todo_id}",
    response_model=schemas.Todo,
    tags=["todos"]
)
def update_todo(
    todo_id: int,
    updates: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    # Apply partial updates
    if updates.title is not None:
        todo.title = updates.title
    if updates.description is not None:
        todo.description = updates.description
    if updates.completed is not None:
        todo.completed = updates.completed

    db.commit()
    db.refresh(todo)
    return todo


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["todos"]
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    db.delete(todo)
    db.commit()
    return None
