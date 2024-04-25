from fastapi import FastAPI, HTTPException, Request, Form, Cookie, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta

#cd C:\Users\ayon4\470\CSE470-Project
#python -m uvicorn main:app --reload
#git clone https://github.com/Shahriar2611/CSE470-Project


app = FastAPI()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = MongoClient("mongodb://mongo:27017/")
db = client["user_db"]
users_collection = db["users"]

SECRET_KEY = "8d42ac633c2be72c96206ff593faa101d04e0d3c2086341d065a3de2a90513d1"
COOKIE_NAME = "session_token"
SESSION_EXPIRE_MINUTES = 30

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse("/login")

# Route handler for the root path "/"
@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

# Route handler for the favicon.ico request
@app.get("/favicon.ico")
async def favicon():
    return {"message": "Favicon not found"}

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session_token: str = Cookie(None)):
    if not is_authenticated(session_token):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {"request": request})

security = HTTPBasic()

class User(BaseModel):
    firstName: str
    lastName: str
    birthdate: str
    email: str
    password: str

@app.post("/register")
async def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Check if username or email already exists
    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Hash password
    hashed_password = bcrypt.hash(password)

    # Insert user into database
    user_data = {"username": username, "email": email, "password": hashed_password}
    users_collection.insert_one(user_data)

    return {"message": "Registration successful"}

@app.post("/login")
async def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    # Create session token
    session_token = create_session_token(username)
    response.set_cookie(key=COOKIE_NAME, value=session_token, httponly=True, max_age=SESSION_EXPIRE_MINUTES * 60)
    return RedirectResponse(url="/dashboard")

def authenticate_user(username: str, password: str):
    # Dummy user data (replace with database lookup)
    fake_users_db = {
        "user1": {
            "username": "user1",
            "hashed_password": "$2b$12$AqIkz4Ne1T/2OiDl5cSEPe/.wuSUW4R/nThLs2aMg1KT58VlUQZ0m"  # Hashed password: password123
        },
        "user2": {
            "username": "user2",
            "hashed_password": "$2b$12$1F/vpswPrrbJWVwUPlA38ORXsbVXYcmIKrWcBQeBoPKqTKCXDaKsG"  # Hashed password: secret456
        }
    }
    if username in fake_users_db:
        user = fake_users_db[username]
        if pwd_context.verify(password, user["hashed_password"]):
            return user
    return None

def create_session_token(username: str):
    expiration_datetime = datetime.utcnow() + timedelta(minutes=SESSION_EXPIRE_MINUTES)
    data = {"sub": username, "exp": expiration_datetime}
    return data["sub"]

def is_authenticated(session_token: str):
    return session_token is not None



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
