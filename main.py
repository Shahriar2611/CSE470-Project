from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
db = client["user_db"]
users_collection = db["users"]

security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    user_exists = users_collection.find_one({"username": user.username})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    user_dict = user.dict()
    user_dict["password"] = user.password  # In a real application, you would hash the password
    user_id = users_collection.insert_one(user_dict).inserted_id
    return {"message": "User registered successfully", "user_id": str(user_id)}

@app.post("/login")
async def login(user_post: User):
    user_db = users_collection.find_one({"username": user_post.username})
    print("user--->",user_db)
    if not user_db or user_db["password"] != user_post.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
