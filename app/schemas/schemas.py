from pydantic import BaseModel, EmailStr,Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import date
from datetime import datetime




class UserBase(BaseModel):
    email: EmailStr
    verification_code: Optional[str] = None
    code_expiration: Optional[str] = None

class UserCreate(UserBase):
    role_ids: List[int] = []

class User(UserBase):
    id: int


    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class RefreshTokenSchema(BaseModel):
    access_token: str
    token_type: str

class EmailBody(BaseModel):
    email: str

class Verify(BaseModel):
    email: str
    code: str



class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    username: str
    field_of_work: Optional[str] = None  
    

class ProfileResponse(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    field_of_work: Optional[str] = None


class ChatResponse(BaseModel):
    partner_id: int
    partner_username: str
    last_message_time: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True



class GroupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the group")
    description: str = Field(None, max_length=500, description="Description of the group")


class TodoBase(BaseModel):
    title: str
    description: str
    status: Optional[bool] = False


class TodoUpdate(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: bool

    class Config:
        orm_mode = True


class Message(BaseModel):
    sender: str
    receiver: str
    content: str