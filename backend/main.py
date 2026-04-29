from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

app = FastAPI()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memory
user_memory = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
You are NutriBot-AI 🥗

Rules (STRICT):
1. Keep answers SHORT (max 8-9 lines)
2. Use simple formatting:
   🔹 Goal:
   🍽️ Diet:
   📊 Tips:
3. Use bullet points ONLY
4. No paragraphs ❌
5. No long explanations ❌
6. Be clear and concise
7. Maintain the line space properly and the format for points
8. Every point must be in next line don't continue in the same line
"""

@app.post("/chat")
async def chat(req: ChatRequest):
    user_id = req.user_id
    message = req.message

    if user_id not in user_memory:
        user_memory[user_id] = {"history": []}

    history = user_memory[user_id]["history"]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history[-5:],
        {"role": "user", "content": message}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=250,
            temperature=0.5
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        reply = "⚠️ AI error. Check API key."

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    return {"response": reply}