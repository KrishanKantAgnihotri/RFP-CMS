from typing import List, Dict, Any, Optional
import logging
import smtplib
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

from app.core.config import settings
from app.db.mongodb import notifications_collection, users_collection
from app.models.notification import Notification
from bson import ObjectId

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any],
    ) -> bool:
        """Send email using configured email provider"""
        try:
            # Render email template
            env = Environment(loader=FileSystemLoader("app/templates"))
            template = env.get_template(f"{template_name}.html")
            html_content = template.render(**template_data)
            
            if settings.EMAIL_PROVIDER == "sendgrid":
                return await NotificationService._send_with_sendgrid(to_email, subject, html_content)
            elif settings.EMAIL_PROVIDER == "mailgun":
                return await NotificationService._send_with_mailgun(to_email, subject, html_content)
            elif settings.EMAIL_PROVIDER == "aws_ses":
                return await NotificationService._send_with_aws_ses(to_email, subject, html_content)
            else:
                logger.warning(f"Unsupported email provider: {settings.EMAIL_PROVIDER}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    async def _send_with_sendgrid(to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SendGrid"""
        try:
            if not settings.SENDGRID_API_KEY:
                logger.error("SendGrid API key not configured")
                return False
            
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                "Content-Type": "application/json",
            }
            data = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": settings.EMAIL_SENDER},
                "subject": subject,
                "content": [{"type": "text/html", "value": html_content}],
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response.status_code == 202
                
        except Exception as e:
            logger.error(f"SendGrid error: {str(e)}")
            return False
    
    @staticmethod
    async def _send_with_mailgun(to_email: str, subject: str, html_content: str) -> bool:
        """Send email using Mailgun"""
        try:
            if not settings.MAILGUN_API_KEY or not settings.MAILGUN_DOMAIN:
                logger.error("Mailgun credentials not configured")
                return False
            
            url = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"
            auth = ("api", settings.MAILGUN_API_KEY)
            data = {
                "from": settings.EMAIL_SENDER,
                "to": to_email,
                "subject": subject,
                "html": html_content,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, auth=auth, data=data)
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"Mailgun error: {str(e)}")
            return False
    
    @staticmethod
    async def _send_with_aws_ses(to_email: str, subject: str, html_content: str) -> bool:
        """Send email using AWS SES"""
        # This is a simplified implementation
        # In production, you would use boto3 or a similar library
        try:
            # Create message
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = settings.EMAIL_SENDER
            msg["To"] = to_email
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, "html"))
            
            # Send email
            with smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", 587) as server:
                server.starttls()
                server.login(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            logger.error(f"AWS SES error: {str(e)}")
            return False
    
    @staticmethod
    async def create_notification(
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        data: Dict[str, Any] = {},
        send_immediately: bool = True,
    ) -> Optional[str]:
        """Create a notification and optionally send it immediately"""
        try:
            # Create notification
            notification = {
                "user_id": ObjectId(user_id),
                "type": notification_type,
                "title": title,
                "message": message,
                "data": data,
                "is_read": False,
                "is_sent": False,
                "created_at": datetime.utcnow(),
            }
            
            result = await notifications_collection().insert_one(notification)
            notification_id = str(result.inserted_id)
            
            # Send notification immediately if requested
            if send_immediately:
                await NotificationService.send_notification(notification_id)
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            return None
    
    @staticmethod
    async def send_notification(notification_id: str) -> bool:
        """Send a notification by its ID"""
        try:
            # Fetch notification
            notification = await notifications_collection().find_one({"_id": ObjectId(notification_id)})
            
            if not notification:
                logger.error(f"Notification not found: {notification_id}")
                return False
            
            # If already sent, do nothing
            if notification["is_sent"]:
                return True
            
            # Fetch user
            user = await users_collection().find_one({"_id": notification["user_id"]})
            
            if not user:
                logger.error(f"User not found for notification: {notification_id}")
                return False
            
            # Send based on notification type
            success = False
            if notification["type"] == "email":
                success = await NotificationService.send_email(
                    user["email"],
                    notification["title"],
                    "notification",  # template name
                    {
                        "title": notification["title"],
                        "message": notification["message"],
                        "user": user,
                        "data": notification["data"],
                    },
                )
            elif notification["type"] == "in_app":
                # In-app notifications don't need to be sent externally
                success = True
            
            # Update notification status
            if success:
                await notifications_collection().update_one(
                    {"_id": ObjectId(notification_id)},
                    {
                        "$set": {
                            "is_sent": True,
                            "sent_at": datetime.utcnow(),
                        }
                    },
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False
    
    @staticmethod
    async def notify_new_rfp(rfp_id: str, rfp_title: str) -> List[str]:
        """Notify all suppliers about a new RFP"""
        try:
            # Find all suppliers
            suppliers = await users_collection().find({"role": "Supplier"}).to_list(length=1000)
            
            notification_ids = []
            for supplier in suppliers:
                notification_id = await NotificationService.create_notification(
                    str(supplier["_id"]),
                    "email",
                    "New RFP Available",
                    f"A new RFP '{rfp_title}' has been published that may be of interest to you.",
                    {"rfp_id": rfp_id, "rfp_title": rfp_title},
                    True,  # send immediately
                )
                
                if notification_id:
                    notification_ids.append(notification_id)
            
            return notification_ids
            
        except Exception as e:
            logger.error(f"Failed to notify suppliers about new RFP: {str(e)}")
            return []
    
    @staticmethod
    async def notify_rfp_response(rfp_id: str, rfp_title: str, supplier_id: str) -> Optional[str]:
        """Notify RFP owner about a new response"""
        try:
            from app.db.mongodb import rfps_collection
            
            # Find RFP
            rfp = await rfps_collection().find_one({"_id": ObjectId(rfp_id)})
            
            if not rfp:
                logger.error(f"RFP not found: {rfp_id}")
                return None
            
            # Find supplier
            supplier = await users_collection().find_one({"_id": ObjectId(supplier_id)})
            
            if not supplier:
                logger.error(f"Supplier not found: {supplier_id}")
                return None
            
            # Create notification for buyer
            notification_id = await NotificationService.create_notification(
                str(rfp["buyer_id"]),
                "email",
                f"New Response to RFP: {rfp_title}",
                f"A new response has been submitted by {supplier['company_name'] or supplier['email']} for your RFP '{rfp_title}'.",
                {
                    "rfp_id": rfp_id,
                    "rfp_title": rfp_title,
                    "supplier_id": supplier_id,
                    "supplier_name": supplier["company_name"] or supplier["email"],
                },
                True,  # send immediately
            )
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to notify buyer about RFP response: {str(e)}")
            return None
    
    @staticmethod
    async def notify_response_status_change(rfp_id: str, rfp_title: str, supplier_id: str, status: str) -> Optional[str]:
        """Notify supplier about response status change"""
        try:
            # Find supplier
            supplier = await users_collection().find_one({"_id": ObjectId(supplier_id)})
            
            if not supplier:
                logger.error(f"Supplier not found: {supplier_id}")
                return None
            
            # Create notification for supplier
            notification_id = await NotificationService.create_notification(
                str(supplier["_id"]),
                "email",
                f"RFP Response Status Update: {rfp_title}",
                f"Your response to RFP '{rfp_title}' has been {status.lower()}.",
                {
                    "rfp_id": rfp_id,
                    "rfp_title": rfp_title,
                    "status": status,
                },
                True,  # send immediately
            )
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to notify supplier about response status change: {str(e)}")
            return None
