'''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_PATH = os.getenv("DB_PATH","/home/viswaz/workspace/p00/backend/users.db")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "friendsforverwithus@gmail.com"
    MAIL_PASSWORD = "iitdh@123"
    SESSION_TYPE = "filesystem"  # Store sessions on the filesystem
    JWT_SECRET_KEY = "your_jwt_secret_here"  # Change this to a secure key
    JWT_TOKEN_LOCATION = ["headers"]  # Ensures tokens are sent via Authorization header
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Tokens expire in 1 hour
'''

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "your_default_secret_key"
    DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "users.db"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME") or "friendsforverwithus@gmail.com"
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD") or "iitdh@123"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    SESSION_TYPE = "filesystem"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "your_jwt_secret_here"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Tokens expire in 1 hour

