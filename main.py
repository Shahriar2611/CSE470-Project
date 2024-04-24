from fastapi import FastAPI, HTTPException, Form, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

#cd C:\Users\ayon4\470\CSE470-Project
#python -m uvicorn main:app --reload
#git clone https://github.com/Shahriar2611/CSE470-Project


app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = MongoClient("mongodb://mongo:27017/")
db = client["user_db"]
users_collection = db["users"]


app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML pages
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

security = HTTPBasic()

class User(BaseModel):
    firstName: str
    lastName: str
    birthdate: str
    email: str
    password: str

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    user_exists = users_collection.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    user_dict = user.model_dump()
    user_dict["password"] = user.password  # In a real application, you would hash the password
    user_id = users_collection.insert_one(user_dict).inserted_id
    return {"message": "User registered successfully", "user_id": str(user_id)}

@app.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    user_db = users_collection.find_one({"username": username})
    if not user_db or user_db["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
