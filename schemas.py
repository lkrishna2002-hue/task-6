# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(
        default=None,
        example="Milk, bread, eggs"
    )
    completed: bool = Field(default=False, example=False)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, example="New title")
    description: Optional[str] = Field(default=None, example="New description")
    completed: Optional[bool] = Field(default=None, example=True)


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
