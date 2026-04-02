# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from chatbot_logic import chatbot_response

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Chatbot API running 🚀"}

@app.post("/chat")
def chat(msg: Message):
    try:
        print("User:", msg.message)

        reply = chatbot_response(msg.message)

        print("Bot:", reply)

        return {"reply": reply}

    except Exception as e:
        print("ERROR:", str(e))
        return {"reply": "Something went wrong. Please try again."}