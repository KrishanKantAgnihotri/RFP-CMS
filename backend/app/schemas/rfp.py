from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class RFPBase(BaseModel):
    title: str
    description: str
    requirements: Dict[str, Any]
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    tags: List[str] = []

class RFPCreate(RFPBase):
    pass

class RFPUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ["Draft", "Published", "Under Review", "Completed", "Cancelled"]:
            raise ValueError('Status must be one of: Draft, Published, Under Review, Completed, Cancelled')
        return v

class RFPInDB(RFPBase):
    id: str
    buyer_id: str
    status: str
    attachments: List[str] = []
    responses: List[str] = []
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class RFPResponse(RFPInDB):
    pass

class RFPResponseBase(BaseModel):
    content: Dict[str, Any]

class RFPResponseCreate(RFPResponseBase):
    pass

class RFPResponseUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    feedback: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ["Submitted", "Under Review", "Approved", "Rejected"]:
            raise ValueError('Status must be one of: Submitted, Under Review, Approved, Rejected')
        return v

class RFPResponseInDB(RFPResponseBase):
    id: str
    rfp_id: str
    supplier_id: str
    status: str
    attachments: List[str] = []
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class RFPResponseResponse(RFPResponseInDB):
    pass
