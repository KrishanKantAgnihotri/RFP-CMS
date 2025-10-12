import os
from pydantic import EmailStr, validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RFP Contract Management System"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "rfp_cms")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Email settings
    EMAIL_PROVIDER: str = os.getenv("EMAIL_PROVIDER", "sendgrid")  # sendgrid, mailgun, aws_ses
    EMAIL_SENDER: Optional[EmailStr] = os.getenv("EMAIL_SENDER")
    SENDGRID_API_KEY: Optional[str] = os.getenv("SENDGRID_API_KEY")
    MAILGUN_API_KEY: Optional[str] = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN: Optional[str] = os.getenv("MAILGUN_DOMAIN")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # File storage settings
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "local")  # aws_s3, cloudinary, local
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    S3_BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")
    CLOUDINARY_CLOUD_NAME: Optional[str] = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: Optional[str] = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: Optional[str] = os.getenv("CLOUDINARY_API_SECRET")
    
    # Search settings
    SEARCH_PROVIDER: str = os.getenv("SEARCH_PROVIDER", "database")  # elasticsearch, algolia, database
    ELASTICSEARCH_URL: Optional[str] = os.getenv("ELASTICSEARCH_URL")
    ALGOLIA_APP_ID: Optional[str] = os.getenv("ALGOLIA_APP_ID")
    ALGOLIA_API_KEY: Optional[str] = os.getenv("ALGOLIA_API_KEY")
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
