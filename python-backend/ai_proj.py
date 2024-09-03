from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
client = OpenAI()
app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(message: Message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": message.content
            }
        ]
    )
    return {"response": completion.choices[0].message.content}


