from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List, Dict, Any

from app.core.config import settings
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse, Token
from app.db.mongodb import users_collection, Database

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    return {"message": "Users endpoint is working", "db_connected": Database.db is not None}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    # Check if user already exists
    existing_user = await users_collection().find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    # Create new user
    from datetime import datetime
    hashed_password = get_password_hash(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    user_data["is_active"] = True
    user_data["is_verified"] = False
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()
    
    result = await users_collection().insert_one(user_data)
    
    # Fetch the created user
    created_user = await users_collection().find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for the response
    user_response = {**created_user}
    user_response["id"] = str(created_user["_id"])
    del user_response["_id"]
    del user_response["hashed_password"]
    
    return user_response

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by email
    user = await users_collection().find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user["_id"]), expires_delta=access_token_expires
    )
    
    # Convert ObjectId to string for the response
    user_response = {**user}
    user_response["id"] = str(user["_id"])
    del user_response["_id"]
    del user_response["hashed_password"]
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response,
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    # Convert ObjectId to string for the response
    user_response = {**current_user}
    user_response["id"] = str(current_user["_id"])
    
    del user_response["_id"]
    del user_response["hashed_password"]
    
    return user_response

@router.put("/me", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Update user
    user_data = user_update.model_dump(exclude_unset=True)
    
    if user_data:
        await users_collection().update_one(
            {"_id": current_user["_id"]},
            {"$set": user_data}
        )
    
    # Fetch updated user
    updated_user = await users_collection().find_one({"_id": current_user["_id"]})
    
    # Convert ObjectId to string for the response
    user_response = {**updated_user}
    user_response["id"] = str(updated_user["_id"])
    del user_response["_id"]
    del user_response["hashed_password"]
    
    return user_response
