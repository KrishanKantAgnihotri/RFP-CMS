from datetime import datetime, timedelta
from typing import Optional, Union, Any, Dict

from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from bson import ObjectId

from app.core.config import settings
from app.schemas.user import TokenData
from app.db.mongodb import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"Received token: {token[:20]}..." if token else "No token received")
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        print(f"Decoded user_id: {user_id}")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except (jwt.JWTError, ValidationError) as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception
    
    try:
        # Convert string user_id back to ObjectId for MongoDB query
        user_object_id = ObjectId(token_data.user_id)
        user = await users_collection().find_one({"_id": user_object_id})
    except Exception:
        raise credentials_exception
        
    if user is None:
        raise credentials_exception
    
    if not user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user
