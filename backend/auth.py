'''import jwt
import datetime
from flask import jsonify
from passlib.context import CryptContext
from config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# 🔹 Password Hashing Functions
def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(username: str, expires_minutes=15) -> str:
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
'''

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

