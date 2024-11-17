from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.config.database.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/search", response_model=List[UserResponse])
def search_users(username: str, db: Session = Depends(get_db)):

    users = db.query(User).filter(User.profile.has(username=username)).all()
    return users
