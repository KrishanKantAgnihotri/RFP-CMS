from datetime import datetime
from typing import Optional, List
from pydantic import Field
from bson import ObjectId
from app.models.base import PyObjectId, BaseModel

class Document(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str
    content_type: str
    user_id: PyObjectId
    rfp_id: Optional[PyObjectId] = None
    response_id: Optional[PyObjectId] = None
    is_public: bool = False
    version: int = 1
    previous_versions: List[PyObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "filename": "f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
                "original_filename": "proposal_document.pdf",
                "file_path": "uploads/documents/f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
                "file_size": 1024000,
                "file_type": "pdf",
                "content_type": "application/pdf",
                "is_public": False,
                "version": 1
            }
        }
