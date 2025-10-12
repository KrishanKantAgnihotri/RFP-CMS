# RFP Contract Management System - Complete Setup Guide

This guide provides detailed instructions for setting up and running the RFP Contract Management System on a new computer.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.9+**
- **Node.js 14+** and **npm 6+**
- **MongoDB 4.4+**

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/RFP_CMS.git
cd RFP_CMS
```

## Step 2: Set Up MongoDB

### Option 1: Manual Installation

1. Download MongoDB Community Edition from the [official website](https://www.mongodb.com/try/download/community)
2. Follow the installation instructions for your operating system
3. Create data directories:
   ```bash
   mkdir -p C:\data\db
   mkdir -p C:\data\log
   ```
4. Start MongoDB:
   ```bash
   "C:\Program Files\MongoDB\Server\{version}\bin\mongod.exe" --dbpath="C:\data\db"
   ```

### Option 2: Using the Provided Script (Windows)

1. Navigate to the scripts directory:
   ```bash
   cd scripts
   ```
2. Run the MongoDB installation script:
   ```bash
   powershell -ExecutionPolicy Bypass -File .\install_mongodb.ps1
   ```

## Step 3: Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory:
   ```bash
   # Windows
   copy .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

5. Edit the `.env` file and replace the following values:
   ```
   # Replace with a strong, random secret key
   SECRET_KEY=your-secret-key-for-jwt

   # Email provider settings (choose one)
   EMAIL_PROVIDER=sendgrid  # Options: sendgrid, mailgun, aws_ses
   EMAIL_SENDER=your-email@example.com
   SENDGRID_API_KEY=your-sendgrid-api-key
   # MAILGUN_API_KEY=your-mailgun-api-key
   # MAILGUN_DOMAIN=your-mailgun-domain
   # AWS_ACCESS_KEY_ID=your-aws-access-key
   # AWS_SECRET_ACCESS_KEY=your-aws-secret-key

   # File storage settings
   STORAGE_PROVIDER=local  # Options: aws_s3, cloudinary, local
   # S3_BUCKET_NAME=your-s3-bucket
   # CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   # CLOUDINARY_API_KEY=your-cloudinary-api-key
   # CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   ```

6. Create the uploads directory:
   ```bash
   mkdir uploads
   ```

## Step 4: Set Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Step 5: Start the Application

1. Start the backend server:
   ```bash
   # From the backend directory with virtual environment activated
   uvicorn app.main:app --reload
   ```
   The backend API will be available at http://localhost:8000.

2. In a new terminal, start the frontend server:
   ```bash
   # From the frontend directory
   npm start
   ```
   The frontend application will be available at http://localhost:3000.

## Step 6: Create Demo Accounts

1. With the backend server running, create demo accounts using curl or any API client:

```bash
# Register buyer account
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

## Step 7: Access the Application

1. Open your web browser and navigate to http://localhost:3000
2. Log in using the demo accounts you just created:
   - Buyer: buyer@test.com / password123
   - Supplier: supplier@test.com / password123

## Key Files and Directories

### Backend

- `backend/app/main.py`: Main application entry point
- `backend/app/core/config.py`: Configuration settings
- `backend/app/api/endpoints/`: API route handlers
- `backend/app/models/`: Database models
- `backend/app/schemas/`: Pydantic schemas for request/response validation
- `backend/app/services/`: Business logic services
- `backend/app/db/`: Database connection and utilities
- `backend/.env`: Environment variables (created during setup)

### Frontend

- `frontend/src/App.tsx`: Main application component
- `frontend/src/context/AuthContext.tsx`: Authentication context
- `frontend/src/pages/`: Page components
- `frontend/src/components/`: Reusable UI components
- `frontend/src/services/api.ts`: API service for backend communication

## Security Considerations

### Keys and Secrets to Replace

1. **JWT Secret Key**:
   - File: `backend/.env`
   - Variable: `SECRET_KEY`
   - Replace with a strong, random string (at least 32 characters)

2. **Email Provider API Keys**:
   - File: `backend/.env`
   - Variables: `SENDGRID_API_KEY`, `MAILGUN_API_KEY`, etc.
   - Replace with your actual API keys from the respective services

3. **Cloud Storage Keys** (if using cloud storage):
   - File: `backend/.env`
   - Variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc.
   - Replace with your actual API keys from the respective services

### Best Practices

1. **Never commit the `.env` file to version control**
2. **Use strong, unique passwords for demo accounts in production**
3. **Implement proper CORS settings in production**
4. **Set up HTTPS for production deployments**

## Troubleshooting

### Backend Issues

1. **MongoDB Connection Error**:
   - Ensure MongoDB is running
   - Check the MongoDB connection URL in `.env`

2. **Module Import Error**:
   - Ensure all dependencies are installed
   - Check that the virtual environment is activated

### Frontend Issues

1. **API Connection Error**:
   - Ensure the backend server is running
   - Check the proxy setting in `package.json`

2. **Missing Dependencies**:
   - Run `npm install` to install all dependencies

## Production Deployment

For production deployment, refer to the [Productionization Guide](./Productionization_guide.md) for detailed instructions on deploying the application to various platforms.

## Additional Resources

- [Quick Start Guide](./Quick_Start_Guide.md)
- [API Documentation](./api-docs.md)
- [Database Schema](./database-schema.md)
- [Productionization Guide](./Productionization_guide.md)
- [Project Summary](./Project_Summary.md)
- [AI Usage Report](./AI_Usage_Report.md)
