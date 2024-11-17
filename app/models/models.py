from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean,UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    verification_code = Column(String, nullable=True)
    code_expiration = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)  
    created_at = Column(DateTime, default=datetime.utcnow) 


    profile = relationship("Profile", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active}, created_at={self.created_at})>"

    @property
    def username(self):
        return self.profile.username if self.profile else None



class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    field_of_work = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))


    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, username={self.username})>"

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    messages = relationship("Message", back_populates="group")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="messages")