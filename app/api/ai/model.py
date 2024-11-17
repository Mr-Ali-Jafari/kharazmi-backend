from fastapi import APIRouter, HTTPException
from transformers import pipeline
from pydantic import BaseModel
import requests

router = APIRouter(
    tags=['ai model'],
    prefix='/ai'
)

HF_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

class ChatRequest(BaseModel):
    prompt: str

def get_chat_response(prompt: str):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = get_chat_response(request.prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
