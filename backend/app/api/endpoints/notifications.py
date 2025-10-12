from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId

from app.core.auth import get_current_user
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from app.db.mongodb import notifications_collection

router = APIRouter()

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_in: NotificationCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Only allow creating notifications for the current user
    if notification_in.user_id != str(current_user["_id"]) and current_user["role"] != "Buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Create notification
    notification_data = notification_in.dict()
    notification_data["user_id"] = ObjectId(notification_in.user_id)
    notification_data["is_read"] = False
    notification_data["is_sent"] = False
    notification_data["created_at"] = datetime.utcnow()
    
    result = await notifications_collection().insert_one(notification_data)
    
    # Fetch created notification
    created_notification = await notifications_collection().find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for the response
    notification_response = {**created_notification}
    notification_response["id"] = str(created_notification["_id"])
    notification_response["user_id"] = str(created_notification["user_id"])
    del notification_response["_id"]
    
    return notification_response

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    is_read: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Build query
    query = {"user_id": current_user["_id"]}
    
    # Filter by is_read if provided
    if is_read is not None:
        query["is_read"] = is_read
    
    # Fetch notifications
    cursor = notifications_collection().find(query).skip(skip).limit(limit).sort("created_at", -1)
    notifications = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for the response
    notification_responses = []
    for notification in notifications:
        notification_response = {**notification}
        notification_response["id"] = str(notification["_id"])
        notification_response["user_id"] = str(notification["user_id"])
        del notification_response["_id"]
        notification_responses.append(notification_response)
    
    return notification_responses

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch notification
    notification = await notifications_collection().find_one({"_id": ObjectId(notification_id)})
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    # Check permissions
    if str(notification["user_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Convert ObjectId to string for the response
    notification_response = {**notification}
    notification_response["id"] = str(notification["_id"])
    notification_response["user_id"] = str(notification["user_id"])
    del notification_response["_id"]
    
    return notification_response

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: str,
    notification_update: NotificationUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Fetch notification
    notification = await notifications_collection().find_one({"_id": ObjectId(notification_id)})
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    # Check permissions
    if str(notification["user_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Update notification
    notification_data = notification_update.dict(exclude_unset=True)
    
    # Set read_at if marking as read
    if notification_data.get("is_read") and not notification["is_read"]:
        notification_data["read_at"] = datetime.utcnow()
    
    # Set sent_at if marking as sent
    if notification_data.get("is_sent") and not notification["is_sent"]:
        notification_data["sent_at"] = datetime.utcnow()
    
    if notification_data:
        await notifications_collection().update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": notification_data}
        )
    
    # Fetch updated notification
    updated_notification = await notifications_collection().find_one({"_id": ObjectId(notification_id)})
    
    # Convert ObjectId to string for the response
    notification_response = {**updated_notification}
    notification_response["id"] = str(updated_notification["_id"])
    notification_response["user_id"] = str(updated_notification["user_id"])
    del notification_response["_id"]
    
    return notification_response

@router.put("/read-all", response_model=Dict[str, Any])
async def mark_all_as_read(
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Mark all notifications as read
    result = await notifications_collection().update_many(
        {
            "user_id": current_user["_id"],
            "is_read": False
        },
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    return {"modified_count": result.modified_count}
