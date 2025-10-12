from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId

from app.core.auth import get_current_user
from app.schemas.rfp import (
    RFPCreate,
    RFPUpdate,
    RFPResponse,
    RFPResponseCreate,
    RFPResponseUpdate,
    RFPResponseResponse,
)
from app.db.mongodb import rfps_collection, users_collection

router = APIRouter()

@router.post("/", response_model=RFPResponse, status_code=status.HTTP_201_CREATED)
async def create_rfp(
    rfp_in: RFPCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Only buyers can create RFPs
    if current_user["role"] != "Buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyers can create RFPs",
        )
    
    # Create new RFP
    rfp_data = rfp_in.dict()
    rfp_data["buyer_id"] = current_user["_id"]
    rfp_data["status"] = "Draft"
    rfp_data["created_at"] = datetime.utcnow()
    rfp_data["updated_at"] = datetime.utcnow()
    rfp_data["attachments"] = []
    rfp_data["responses"] = []
    
    result = await rfps_collection().insert_one(rfp_data)
    
    # Fetch the created RFP
    created_rfp = await rfps_collection().find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for the response
    rfp_response = {**created_rfp}
    rfp_response["id"] = str(created_rfp["_id"])
    rfp_response["buyer_id"] = str(created_rfp["buyer_id"])
    del rfp_response["_id"]
    
    return rfp_response

@router.get("/", response_model=List[RFPResponse])
async def get_rfps(
    status: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Build query
    query = {}
    
    # Filter by status if provided
    if status:
        query["status"] = status
    
    # Filter by category if provided
    if category:
        query["category"] = category
    
    # For suppliers, only show published RFPs
    if current_user["role"] == "Supplier":
        query["status"] = "Published"
    
    # For buyers, show only their RFPs
    if current_user["role"] == "Buyer":
        query["buyer_id"] = current_user["_id"]
    
    # Fetch RFPs
    cursor = rfps_collection().find(query).skip(skip).limit(limit).sort("created_at", -1)
    rfps = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for the response
    rfp_responses = []
    for rfp in rfps:
        rfp_response = {**rfp}
        rfp_response["id"] = str(rfp["_id"])
        rfp_response["buyer_id"] = str(rfp["buyer_id"])
        rfp_response["responses"] = [str(resp) for resp in rfp.get("responses", [])]
        del rfp_response["_id"]
        rfp_responses.append(rfp_response)
    
    return rfp_responses

@router.get("/{rfp_id}", response_model=RFPResponse)
async def get_rfp(
    rfp_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch RFP
    rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
    
    if not rfp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RFP not found",
        )
    
    # Check access permissions
    if current_user["role"] == "Supplier" and rfp["status"] != "Published":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    if current_user["role"] == "Buyer" and str(rfp["buyer_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Convert ObjectId to string for the response
    rfp_response = {**rfp}
    rfp_response["id"] = str(rfp["_id"])
    rfp_response["buyer_id"] = str(rfp["buyer_id"])
    rfp_response["responses"] = [str(resp) for resp in rfp.get("responses", [])]
    del rfp_response["_id"]
    
    return rfp_response

@router.put("/{rfp_id}", response_model=RFPResponse)
async def update_rfp(
    rfp_id: str,
    rfp_update: RFPUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch RFP
    rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
    
    if not rfp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RFP not found",
        )
    
    # Only the owner can update the RFP
    if str(rfp["buyer_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Update RFP
    rfp_data = rfp_update.dict(exclude_unset=True)
    rfp_data["updated_at"] = datetime.utcnow()
    
    # If status is changing to Published, set published_at
    if rfp_data.get("status") == "Published" and rfp["status"] != "Published":
        rfp_data["published_at"] = datetime.utcnow()
    
    if rfp_data:
        await rfps_collection().update_one(
            {"_id": ObjectId(rfp_id)},
            {"$set": rfp_data}
        )
    
    # Fetch updated RFP
    updated_rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
    
    # Convert ObjectId to string for the response
    rfp_response = {**updated_rfp}
    rfp_response["id"] = str(updated_rfp["_id"])
    rfp_response["buyer_id"] = str(updated_rfp["buyer_id"])
    rfp_response["responses"] = [str(resp) for resp in updated_rfp.get("responses", [])]
    del rfp_response["_id"]
    
    return rfp_response

@router.post("/{rfp_id}/responses", response_model=RFPResponseResponse, status_code=status.HTTP_201_CREATED)
async def create_rfp_response(
    rfp_id: str,
    response_in: RFPResponseCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Only suppliers can respond to RFPs
    if current_user["role"] != "Supplier":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only suppliers can respond to RFPs",
        )
    
    # Fetch RFP
    rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
    
    if not rfp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RFP not found",
        )
    
    # Check if RFP is published
    if rfp["status"] != "Published":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot respond to unpublished RFP",
        )
    
    # Check if supplier has already responded
    existing_response = await rfps_collection().find_one({
        "_id": ObjectId(rfp_id),
        "responses.supplier_id": current_user["_id"]
    })
    
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already responded to this RFP",
        )
    
    # Create new response
    response_data = response_in.dict()
    response_data["rfp_id"] = ObjectId(rfp_id)
    response_data["supplier_id"] = current_user["_id"]
    response_data["status"] = "Submitted"
    response_data["created_at"] = datetime.utcnow()
    response_data["updated_at"] = datetime.utcnow()
    response_data["attachments"] = []
    
    # Insert response
    result = await rfps_collection().update_one(
        {"_id": ObjectId(rfp_id)},
        {
            "$push": {"responses": response_data},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create response",
        )
    
    # Convert ObjectId to string for the response
    response_data["id"] = str(response_data["rfp_id"]) + "-" + str(response_data["supplier_id"])
    response_data["rfp_id"] = str(response_data["rfp_id"])
    response_data["supplier_id"] = str(response_data["supplier_id"])
    
    return response_data

@router.get("/{rfp_id}/responses", response_model=List[RFPResponseResponse])
async def get_rfp_responses(
    rfp_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch RFP
    rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
    
    if not rfp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RFP not found",
        )
    
    # Check access permissions
    if current_user["role"] == "Buyer" and str(rfp["buyer_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    if current_user["role"] == "Supplier":
        # Suppliers can only see their own responses
        responses = [resp for resp in rfp.get("responses", []) if str(resp["supplier_id"]) == str(current_user["_id"])]
    else:
        # Buyers can see all responses
        responses = rfp.get("responses", [])
    
    # Convert ObjectId to string for the response
    response_list = []
    for resp in responses:
        resp_data = {**resp}
        resp_data["id"] = str(resp["rfp_id"]) + "-" + str(resp["supplier_id"])
        resp_data["rfp_id"] = str(resp["rfp_id"])
        resp_data["supplier_id"] = str(resp["supplier_id"])
        response_list.append(resp_data)
    
    return response_list
