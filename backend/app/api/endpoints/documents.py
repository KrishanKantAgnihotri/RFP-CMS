from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import shutil
import uuid
from bson import ObjectId
import aiofiles

from app.core.config import settings
from app.core.auth import get_current_user
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.db.mongodb import documents_collection, rfps_collection

router = APIRouter()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    rfp_id: Optional[str] = Form(None),
    response_id: Optional[str] = Form(None),
    is_public: bool = Form(False),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Check if RFP exists if rfp_id is provided
    if rfp_id:
        rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
        if not rfp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RFP not found",
            )
        
        # Check permissions
        if current_user["role"] == "Buyer" and str(rfp["buyer_id"]) != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create directory structure
    year_month = datetime.utcnow().strftime("%Y/%m")
    upload_dir = os.path.join(settings.UPLOAD_FOLDER, year_month)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    
    async with aiofiles.open(file_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
    
    # Create document record
    document_data = {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_path": file_path,
        "file_size": os.path.getsize(file_path),
        "file_type": file_extension.lstrip(".").lower(),
        "content_type": file.content_type,
        "user_id": current_user["_id"],
        "is_public": is_public,
        "version": 1,
        "previous_versions": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    if rfp_id:
        document_data["rfp_id"] = ObjectId(rfp_id)
    
    if response_id:
        document_data["response_id"] = ObjectId(response_id)
    
    # Insert document
    result = await documents_collection().insert_one(document_data)
    
    # Update RFP with attachment reference if rfp_id is provided
    if rfp_id:
        await rfps_collection().update_one(
            {"_id": ObjectId(rfp_id)},
            {"$push": {"attachments": str(result.inserted_id)}}
        )
    
    # Fetch created document
    created_document = await documents_collection().find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for the response
    doc_response = {**created_document}
    doc_response["id"] = str(created_document["_id"])
    doc_response["user_id"] = str(created_document["user_id"])
    
    if "rfp_id" in created_document:
        doc_response["rfp_id"] = str(created_document["rfp_id"])
    
    if "response_id" in created_document:
        doc_response["response_id"] = str(created_document["response_id"])
    
    del doc_response["_id"]
    
    return doc_response

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    rfp_id: Optional[str] = None,
    response_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Build query
    query = {}
    
    # Filter by rfp_id if provided
    if rfp_id:
        query["rfp_id"] = ObjectId(rfp_id)
    
    # Filter by response_id if provided
    if response_id:
        query["response_id"] = ObjectId(response_id)
    
    # For non-public documents, check permissions
    if current_user["role"] == "Supplier":
        query["$or"] = [
            {"is_public": True},
            {"user_id": current_user["_id"]}
        ]
    
    # Fetch documents
    cursor = documents_collection().find(query).skip(skip).limit(limit).sort("created_at", -1)
    documents = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for the response
    doc_responses = []
    for doc in documents:
        doc_response = {**doc}
        doc_response["id"] = str(doc["_id"])
        doc_response["user_id"] = str(doc["user_id"])
        
        if "rfp_id" in doc:
            doc_response["rfp_id"] = str(doc["rfp_id"])
        
        if "response_id" in doc:
            doc_response["response_id"] = str(doc["response_id"])
        
        del doc_response["_id"]
        doc_responses.append(doc_response)
    
    return doc_responses

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch document
    document = await documents_collection().find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Check permissions
    if not document["is_public"] and str(document["user_id"]) != str(current_user["_id"]):
        # If document is associated with an RFP, check if user is the RFP owner
        if "rfp_id" in document:
            rfp = await rfps_collection().find_one({"_id": document["rfp_id"]})
            if not rfp or str(rfp["buyer_id"]) != str(current_user["_id"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    # Convert ObjectId to string for the response
    doc_response = {**document}
    doc_response["id"] = str(document["_id"])
    doc_response["user_id"] = str(document["user_id"])
    
    if "rfp_id" in document:
        doc_response["rfp_id"] = str(document["rfp_id"])
    
    if "response_id" in document:
        doc_response["response_id"] = str(document["response_id"])
    
    del doc_response["_id"]
    
    return doc_response

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch document
    document = await documents_collection().find_one({"_id": ObjectId(document_id)})
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    # Check permissions
    if not document["is_public"] and str(document["user_id"]) != str(current_user["_id"]):
        # If document is associated with an RFP, check if user is the RFP owner
        if "rfp_id" in document:
            rfp = await rfps_collection().find_one({"_id": document["rfp_id"]})
            if not rfp or str(rfp["buyer_id"]) != str(current_user["_id"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    # Return file
    return FileResponse(
        path=document["file_path"],
        filename=document["original_filename"],
        media_type=document["content_type"]
    )
