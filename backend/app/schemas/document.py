from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    original_filename: str
    file_type: str
    content_type: str
    is_public: bool = False

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    original_filename: Optional[str] = None
    is_public: Optional[bool] = None

class DocumentInDB(DocumentBase):
    id: str
    filename: str
    file_path: str
    file_size: int
    user_id: str
    rfp_id: Optional[str] = None
    response_id: Optional[str] = None
    version: int
    previous_versions: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class DocumentResponse(DocumentInDB):
    pass
