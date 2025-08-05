import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from urllib.parse import parse_qs

#pip install fastapi python-dotenv
#pip install "uvicorn[standard]"

#python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

# Load environment variables (if using .env)
load_dotenv()

# Load local knowledge base from JSON file
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)


def get_kb_answer(user_message: str) -> str | None:
    """
    Simple keyword-based lookup in the local knowledge base.
    Returns the matching answer if a question keyword is found, else None.
    """
    msg_lower = user_message.lower()
    for entry in knowledge_base:
        question = entry.get("question", "").lower()
        if question and question in msg_lower:
            return entry.get("answer")
    return None

app = FastAPI(title="Rule-based Customer Service Chatbot (Universal Body with CORS)")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        # Read raw request body
        raw_body = await request.body()
        body_str = raw_body.decode("utf-8")

        # Attempt JSON parse
        try:
            data = json.loads(body_str)
            message = data.get("message", body_str)
        except json.JSONDecodeError:
            # Fallback: URL-encoded form
            if "=" in body_str:
                parsed = parse_qs(body_str)
                message = parsed.get("message", [body_str])[0]
            else:
                # Plain text
                message = body_str

        # Rule-based lookup
        kb_answer = get_kb_answer(message)
        if kb_answer:
            reply = kb_answer
        else:
            reply = "I'm sorry, I don't have an answer for that."

        return JSONResponse(content={"reply": reply})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run as a script:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
