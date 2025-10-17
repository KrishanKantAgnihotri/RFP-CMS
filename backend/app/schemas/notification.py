from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    data: Dict[str, Any] = {}
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if v not in ["email", "in_app", "sms"]:
            raise ValueError('Type must be one of: email, in_app, sms')
        return v

class NotificationCreate(NotificationBase):
    user_id: str

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_sent: Optional[bool] = None
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None

class NotificationInDB(NotificationBase):
    id: str
    user_id: str
    is_read: bool
    is_sent: bool
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationResponse(NotificationInDB):
    pass
