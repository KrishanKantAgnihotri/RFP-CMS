from datetime import datetime
from typing import Optional, List
from pydantic import Field
from bson import ObjectId
from app.models.base import PyObjectId, BaseModel

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    username: str
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str  # "Buyer" or "Supplier"
    company_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "role": "Buyer",
                "company_name": "Acme Inc.",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
