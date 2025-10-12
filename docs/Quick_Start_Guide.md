# RFP Contract Management System - Quick Start Guide

This guide provides the essential steps to quickly set up and run the RFP Contract Management System.

## Prerequisites

- Python 3.9+
- Node.js 14+
- MongoDB 4.4+

## 1. Clone and Set Up

```bash
# Clone repository
git clone https://github.com/yourusername/RFP_CMS.git
cd RFP_CMS

# Install MongoDB (if not already installed)
# Windows: Run the installation script
cd scripts
powershell -ExecutionPolicy Bypass -File .\install_mongodb.ps1
cd ..
```

## 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "# API settings
DEBUG=True
ENVIRONMENT=development

# MongoDB settings
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=rfp_cms

# JWT settings
SECRET_KEY=your-secret-key-for-jwt

# Email settings
EMAIL_PROVIDER=sendgrid
EMAIL_SENDER=noreply@example.com
SENDGRID_API_KEY=your-sendgrid-api-key

# File storage settings
STORAGE_PROVIDER=local
UPLOAD_FOLDER=uploads

# Search settings
SEARCH_PROVIDER=database" > .env

# Create uploads directory
mkdir uploads

# Start backend server
uvicorn app.main:app --reload
```

## 3. Frontend Setup (In a New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start frontend server
npm start
```

## 4. Create Demo Accounts

```bash
# Register buyer account (in a new terminal)
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "buyer@test.com",
    "username": "buyer",
    "password": "password123",
    "role": "Buyer",
    "first_name": "John",
    "last_name": "Buyer",
    "company_name": "Buyer Corp"
  }'

# Register supplier account
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "supplier@test.com",
    "username": "supplier",
    "password": "password123",
    "role": "Supplier",
    "first_name": "Jane",
    "last_name": "Supplier",
    "company_name": "Supplier Inc"
  }'
```

## 5. Access the Application

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Login with the demo accounts you created:
  - **Buyer**: buyer@test.com / password123
  - **Supplier**: supplier@test.com / password123

## Important Security Note

Before using in production, replace the following keys in the `.env` file:

- `SECRET_KEY`: Use a strong, random string
- `SENDGRID_API_KEY`: Use your actual SendGrid API key
- Other API keys as needed for your selected services

For detailed setup instructions and production deployment guidance, refer to the [Complete Setup Guide](./Complete_Setup_Guide.md) and [Productionization Guide](./Productionization_guide.md).
