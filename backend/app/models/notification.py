from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import Field
from bson import ObjectId
from app.models.base import PyObjectId, BaseModel

class Notification(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    type: str  # email, in_app, sms
    title: str
    message: str
    data: Dict[str, Any] = {}
    is_read: bool = False
    is_sent: bool = False
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "type": "email",
                "title": "New RFP Published",
                "message": "A new RFP has been published that matches your profile",
                "data": {
                    "rfp_id": "60d21b4967d0d8992e610c85",
                    "rfp_title": "IT Services RFP"
                },
                "is_read": False,
                "is_sent": True,
                "sent_at": "2023-01-01T12:00:00",
                "created_at": "2023-01-01T12:00:00"
            }
        }
