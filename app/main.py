from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.login import login
from app.models.models import Base
from app.config.database import database
from app.api.profile import profile_api
from app.api.ai import model
from app.api.message import websocket
from app.api.user import user











Base.metadata.create_all(bind=database.engine)


app = FastAPI()



origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(login.router)
app.include_router(profile_api.router)
app.include_router(websocket.router)




app.include_router(model.router)





