from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.api.login import login
from app.models.models import Base
from app.config.database import database
from app.api.profile import profile_api
from app.api.ai import model
from app.api.message import websocket,personal
from app.api.user import user
import pickle
from pathlib import Path
from app.api.todo import todo_api
from app.config.database.database import get_db
from app.models.models import User


root_dir = Path(__file__).parent 

data_path = root_dir / 'qa_model.pkl'


with open(data_path, 'rb') as f:
    questions, answers = pickle.load(f)










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
app.include_router(personal.router)
app.include_router(todo_api.router)









def similarity(query, question):
    query_words = set(query.lower().split())
    question_words = set(question.lower().split())
    return len(query_words & question_words) / len(query_words | question_words)

def get_answer(user_question, questions, answers):
    similarities = [similarity(user_question, q) for q in questions]
    if max(similarities) == 0:
        return None
    most_similar_index = similarities.index(max(similarities))
    return answers[most_similar_index]



class QuestionRequest(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(request: QuestionRequest):

    answer = get_answer(request.question, questions, answers)
    if answer:
        return {"question": request.question, "answer": answer}
    else:
        raise HTTPException(status_code=404, detail="No matching question found")





@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.username for user in users]