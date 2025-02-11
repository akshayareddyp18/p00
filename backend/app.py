from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_talisman import Talisman
import os
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp



app = Flask(__name__)
app.config.from_object("config.Config")


'''
app.config["JWT_HEADER_NAME"] = "Authorization"  # Default is 'Authorization'
app.config["JWT_HEADER_TYPE"] = "Bearer"  # Default is 'Bearer'
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_here"
app.config["JWT_ALGORITHM"] = "HS256"
'''



CORS(app, supports_credentials=True)
Talisman(app, content_security_policy=None)


jwt = JWTManager(app)  # ✅ Initialize JWTManager




# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/")




# Define frontend path
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))




@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

'''from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from auth import hash_password, verify_password  # Import functions
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()

# Simulated user database (Use a real database in production)
users_db = {}

SECRET_KEY = "your_secret_key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# User Signup Model
class UserSignup(BaseModel):
    username: str
    password: str
    email: str


# User Login Model
class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/signup")
async def signup(user: UserSignup):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user.password)
    users_db[user.username] = {"email": user.email, "password": hashed_pwd}

    return {"message": "User registered successfully!"}


@app.post("/login")
async def login(user: UserLogin):
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    stored_password = users_db[user.username]["password"]

    if not verify_password(user.password, stored_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate a token (You can use JWT for real authentication)
    token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm="HS256")

    return {"message": "Login successful", "access_token": token}


@app.get("/user-profile")
async def user_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")

        if username not in users_db:
            raise HTTPException(status_code=400, detail="User not found")

        return {"username": username, "email": users_db[username]["email"]}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/logout")
async def logout():
    return {"message": "User logged out successfully"}'''

