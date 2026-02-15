from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory storage
users_db = []

# Request model
class User(BaseModel):
    name: str
    age: int

# Response model
class UserResponse(BaseModel):
    message: str
    data: User


# 1️⃣ Create User
@app.post("/users",
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users_db.append(user)
    return {
        "message": "User created successfully",
        "data": user
    }


# 2️⃣ Get All Users
@app.get("/users", response_model=List[User])
def get_all_users():
    return users_db


# 3️⃣ Get User By Name
@app.get("/users/{name}", response_model=User)
def get_user_by_name(name: str):
    for user in users_db:
        if user.name == name:
            return user

    raise HTTPException(status_code=404, detail="User not found")
