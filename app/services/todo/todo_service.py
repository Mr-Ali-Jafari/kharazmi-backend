from app.models.models import Todo
from app.schemas.schemas import TodoBase,TodoUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException




def create_todo(db: Session, todo: TodoBase, user_id: int):
    db_todo = Todo(title=todo.title, description=todo.description,status=todo.status, user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo: TodoUpdate, user_id: int):
    todo_item = db.query(Todo).filter(Todo.id == todo.id,Todo.user_id == user_id).first()

    if todo.title is not None:
        todo_item.title = todo.title
    if todo.description is not None:
        todo_item.description = todo.description
    if todo.status is not None:
        todo_item.status = todo.status

    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)

    return todo_item