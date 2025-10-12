from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import Field
from bson import ObjectId
from app.models.base import PyObjectId, BaseModel

class RFPResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    rfp_id: PyObjectId
    supplier_id: PyObjectId
    content: Dict[str, Any]
    attachments: List[str] = []
    status: str = "Submitted"  # Submitted, Under Review, Approved, Rejected
    feedback: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RFP(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    buyer_id: PyObjectId
    requirements: Dict[str, Any]
    attachments: List[str] = []
    status: str = "Draft"  # Draft, Published, Under Review, Completed, Cancelled
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    tags: List[str] = []
    responses: List[PyObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "IT Services RFP",
                "description": "Request for proposal for IT services",
                "requirements": {
                    "scope": "Full IT support for 100 employees",
                    "duration": "12 months",
                    "budget": "$50,000"
                },
                "status": "Published",
                "deadline": "2023-12-31T23:59:59",
                "category": "IT Services",
                "tags": ["IT", "Support", "Maintenance"]
            }
        }
