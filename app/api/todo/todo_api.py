from app.models.models import Todo
from app.schemas.schemas import TodoBase,TodoUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database.database import get_db
from app.api.login.login import get_current_user
from app.models.models import User
from app.services.todo.todo_service import create_todo,update_todo


# create an APIRouter instance
router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


# define a route for creating a todo
@router.post("/")
def create_todo_route(data: TodoBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_todo(db=db, todo=data, user_id=current_user.id)


@router.put("/update")
def update_todo_route(data: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_todo(db=db,todo=data,user_id=current_user.id)