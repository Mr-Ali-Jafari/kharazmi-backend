from fastapi import HTTPException, UploadFile,Depends
from sqlalchemy.orm import Session
from app.models.models import Profile, User
from app.schemas.schemas import ProfileCreate, ProfileUpdate,ProfileResponse
from app.api.login.login import get_current_user
import shutil
import os

def create_profile(db: Session, profile: ProfileCreate, user_id: int):
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="این کاربر قبلاً پروفایل دارد.")
    
    db_profile = Profile(
        first_name=profile.first_name,
        last_name=profile.last_name,
        phone_number=profile.phone_number,
        username=profile.username,
        field_of_work=profile.field_of_work,
        user_id=user_id 
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Profile).offset(skip).limit(limit).all()

def get_profile(db: Session, current_user: User = Depends(get_current_user)) -> ProfileResponse:
    db_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

def update_profile(db: Session, profile_id: int, profile: ProfileUpdate):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile:
        if profile.first_name:
            db_profile.first_name = profile.first_name
        if profile.last_name:
            db_profile.last_name = profile.last_name
        if profile.phone_number:
            db_profile.phone_number = profile.phone_number
        if profile.username:
            db_profile.username = profile.username
        if profile.field_of_work:
            db_profile.field_of_work = profile.field_of_work

        db.commit()
        db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return db_profile
