from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = MongoClient("mongodb://localhost:27017/")
db = client["fitness_tracker"]
users_collection = db["users"]
exercises_collection = db["exercises"]
diets_collection = db["diets"]

security = HTTPBasic()

# Check if user is authenticated
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user["username"]

# Authentication function
def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username, "password": password})
    return user

# Homepage
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    return {"message": "Favicon not found"}

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# User login
@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials.username, credentials.password)
    if user:
        return RedirectResponse(url="/dashboard")
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# User registration
@app.post("/register")
async def register(username: str, email: str, password: str):
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = {"username": username, "email": email, "password": password}
    users_collection.insert_one(new_user)
    return {"message": "Registration successful"}

# Dashboard endpoint
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Workout endpoint
@app.get("/workout/", response_class=HTMLResponse)
async def workout(goal: str, request: Request):
    # Fetch exercises based on goal from MongoDB
    exercises = exercises_collection.find({"goal": goal})
    return templates.TemplateResponse("workout.html", {"request": request, "exercises": exercises})

# Diet endpoint
@app.get("/diet/", response_class=HTMLResponse)
async def diet(goal: str, request: Request):
    # Fetch diet plans based on goal from MongoDB
    diets = diets_collection.find({"goal": goal})
    return templates.TemplateResponse("diet.html", {"request": request, "diets": diets})



