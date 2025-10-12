# RFP Contract Management System - Setup Guide

This guide will walk you through the process of setting up the RFP Contract Management System on your local machine for development or testing purposes.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.9+**
- **Node.js 14+** and **npm 6+**
- **MongoDB 4.4+**

## Backend Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/RFP_CMS.git
cd RFP_CMS
```

2. **Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

4. **Create environment variables**

Create a `.env` file in the `backend` directory with the following content:

```
# API settings
DEBUG=True
ENVIRONMENT=development

# MongoDB settings
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=rfp_cms

# JWT settings
SECRET_KEY=your-secret-key-for-jwt

# Email settings (choose one provider)
EMAIL_PROVIDER=sendgrid  # sendgrid, mailgun, aws_ses
EMAIL_SENDER=noreply@example.com
SENDGRID_API_KEY=your-sendgrid-api-key
# MAILGUN_API_KEY=your-mailgun-api-key
# MAILGUN_DOMAIN=your-mailgun-domain
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key

# File storage settings
STORAGE_PROVIDER=local  # aws_s3, cloudinary, local
UPLOAD_FOLDER=uploads
# S3_BUCKET_NAME=your-s3-bucket
# CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
# CLOUDINARY_API_KEY=your-cloudinary-api-key
# CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Search settings
SEARCH_PROVIDER=database  # elasticsearch, algolia, database
# ELASTICSEARCH_URL=http://localhost:9200
# ALGOLIA_APP_ID=your-algolia-app-id
# ALGOLIA_API_KEY=your-algolia-api-key
```

5. **Create uploads directory**

```bash
mkdir uploads
```

6. **Start the backend server**

```bash
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## Frontend Setup

1. **Navigate to the frontend directory**

```bash
cd ../frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Start the development server**

```bash
npm start
```

The frontend application will be available at http://localhost:3000.

## Database Setup

The application will automatically create the required collections in MongoDB when it starts. However, you may want to create some initial data:

1. **Start MongoDB**

Make sure MongoDB is running on your machine.

2. **Create demo accounts**

You can use the API to create the demo accounts:

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

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Troubleshooting

### MongoDB Connection Issues

- Make sure MongoDB is running on your machine
- Verify the connection string in the `.env` file
- Check MongoDB logs for any errors

### Email Sending Issues

- Verify your email provider credentials in the `.env` file
- Check if your email provider has any sending limits or restrictions

### File Upload Issues

- Make sure the `uploads` directory exists and has proper permissions
- Check if there are any file size limitations in your environment

## Next Steps

After setting up the application, you can:

1. Create a new RFP as a buyer
2. Publish the RFP
3. Log in as a supplier and respond to the RFP
4. Review and approve/reject responses as a buyer

For more information on using the application, refer to the [User Guide](./user-guide.md).

For information on deploying the application to production, refer to the [Productionization Guide](./Productionization_guide.md).
