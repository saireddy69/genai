from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# users_list = []

# class User(BaseModel):
#     name: str
#     age: int

# class ResponseModel(BaseModel):
#     message: str
#     data: User

# @app.post('/users',response_model=ResponseModel,status_code=status.HTTP_201_CREATED)
# def create_employees(user: User):
#     users_list.append(user)
#     return {
#         "message": "User created successfully",
#         "data": user
#     }

# @app.get('/users', response_model=List[User])
# def users_data():
#     return users_list

# @app.get("/users/{name}", response_model=User)
# def get_user(name: str):
#     for record in users_list:
#         if record.name == name:
#             return record

#     raise HTTPException(status_code=404, detail="User not found")       

# @app.get("/external-users")
# def get_external_users():
#     url = os.getenv("API_URL")
#     if not url:
#         raise HTTPException(status_code=500, detail="API_URL not configured")

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return data[:3]  # return first 3 users

#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=502, detail=f"External API failed: {str(e)}")

class ChatRequest(BaseModel):
    message: str
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
    user_message = request.message

    # Simulated AI processing
    ai_reply = f"AI says: You said '{user_message}'. This is a simulated response."

    return {
        "reply": ai_reply
    }

