from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas import schemas as schemas
from app.config.database.database import get_db
from app.services.login.login_service import (
    login_with_email_service,
    verify_code_service,
    get_current_user_service,
    refresh_token_service,
)

router = APIRouter(
    prefix="/login",
    tags=['Login']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/verify-code")

@router.post("/send-code", response_model=dict)
def send_verification_code(email: schemas.EmailBody, db: Session = Depends(get_db)):
    try:
        return login_with_email_service(db, email.email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/verify-code", response_model=schemas.Token)
def verify_code(verify: schemas.Verify, db: Session = Depends(get_db)):
    try:
        return verify_code_service(db, verify.email, verify.code)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/current-user", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_current_user_service(db, token)



@router.post("/token/refresh", response_model=schemas.RefreshTokenSchema)
def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        return refresh_token_service(token, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )