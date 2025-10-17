from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class RFPBase(BaseModel):
    title: str
    description: str
    requirements: str
    submission_deadline: datetime
    budget: Optional[float] = None
    categories: Optional[List[str]] = []
    evaluation_criteria: str
    terms_conditions: Optional[str] = None
    status: Optional[str] = "draft"

class RFPCreate(RFPBase):
    pass

class RFPUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    submission_deadline: Optional[datetime] = None
    budget: Optional[float] = None
    categories: Optional[List[str]] = None
    evaluation_criteria: Optional[str] = None
    terms_conditions: Optional[str] = None
    status: Optional[str] = None
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ["draft", "published", "closed", "awarded"]:
            raise ValueError('Status must be one of: draft, published, closed, awarded')
        return v

class RFPInDB(RFPBase):
    id: str
    buyer_id: str
    attachments: List[str] = []
    responses: List[str] = []
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

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
    
    @field_validator('status')
    @classmethod
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
        from_attributes = True

class RFPResponseResponse(RFPResponseInDB):
    pass
