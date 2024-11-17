from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import ProfileCreate, ProfileResponse, ProfileUpdate
from app.config.database.database import get_db
from app.models.models import Profile, User
from app.services.profile.profile_service import create_profile, update_profile, get_profiles, get_profile, delete_profile
from app.api.login.login import get_current_user

router = APIRouter(
    tags=['profile'],
    prefix='/profile'
)

@router.post("/create", response_model=ProfileResponse)
def create_profile_api(profile: ProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="شما قبلاً پروفایل ساخته‌اید.")
    
    existing_username = db.query(Profile).filter(Profile.username == profile.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="یوزرنیم وارد شده قبلاً استفاده شده است.")
    
    return create_profile(db=db, profile=profile, user_id=current_user.id)

@router.get("/profiles", response_model=list[ProfileResponse])
def get_profiles_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_profiles(db=db, skip=skip, limit=limit)

@router.get("/profile", response_model=ProfileResponse)
def get_profile_api(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user
    """
    return get_profile(db=db, current_user=current_user)

@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_profile_api(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if db_profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="شما مجاز به ویرایش این پروفایل نیستید.")
    
    return update_profile(db=db, profile_id=profile_id, profile=profile)

@router.delete("/profiles/{profile_id}", response_model=ProfileResponse)
def delete_profile_api(profile_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if db_profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="شما مجاز به حذف این پروفایل نیستید.")
    
    return delete_profile(db=db, profile_id=profile_id)
