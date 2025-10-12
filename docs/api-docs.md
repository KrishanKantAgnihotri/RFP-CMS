# RFP Contract Management System API Documentation

This document provides details about the API endpoints available in the RFP Contract Management System.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

To obtain a token, use the login endpoint.

## Endpoints

### Authentication

#### Register User

```
POST /users/register
```

Register a new user with buyer or supplier role.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "role": "Buyer",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Company Inc"
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Buyer",
  "company_name": "Company Inc",
  "is_active": true,
  "is_verified": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Login

```
POST /users/login
```

Authenticate a user and get a JWT token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "60d21b4967d0d8992e610c85",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Buyer",
    "company_name": "Company Inc",
    "is_active": true,
    "is_verified": false,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
}
```

#### Get Current User

```
GET /users/me
```

Get the currently authenticated user's information.

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Buyer",
  "company_name": "Company Inc",
  "is_active": true,
  "is_verified": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Update User Profile

```
PUT /users/me
```

Update the current user's profile information.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "company_name": "New Company Inc"
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Smith",
  "role": "Buyer",
  "company_name": "New Company Inc",
  "is_active": true,
  "is_verified": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### RFP Management

#### Create RFP

```
POST /rfps
```

Create a new RFP (Buyer only).

**Request Body:**
```json
{
  "title": "IT Services RFP",
  "description": "Request for proposal for IT services",
  "requirements": {
    "scope": "Full IT support for 100 employees",
    "budget": "$50,000",
    "timeline": "12 months",
    "deliverables": "Monthly reports, 24/7 support"
  },
  "deadline": "2023-12-31T23:59:59",
  "category": "IT Services",
  "tags": ["IT", "Support", "Maintenance"]
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "title": "IT Services RFP",
  "description": "Request for proposal for IT services",
  "buyer_id": "60d21b4967d0d8992e610c85",
  "requirements": {
    "scope": "Full IT support for 100 employees",
    "budget": "$50,000",
    "timeline": "12 months",
    "deliverables": "Monthly reports, 24/7 support"
  },
  "attachments": [],
  "status": "Draft",
  "deadline": "2023-12-31T23:59:59",
  "category": "IT Services",
  "tags": ["IT", "Support", "Maintenance"],
  "responses": [],
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "published_at": null
}
```

#### Get RFPs

```
GET /rfps
```

Get a list of RFPs. Buyers see their own RFPs, suppliers see published RFPs.

**Query Parameters:**
- `status`: Filter by status (optional)
- `category`: Filter by category (optional)
- `skip`: Number of items to skip (pagination)
- `limit`: Number of items to return (pagination)

**Response:**
```json
[
  {
    "id": "60d21b4967d0d8992e610c85",
    "title": "IT Services RFP",
    "description": "Request for proposal for IT services",
    "buyer_id": "60d21b4967d0d8992e610c85",
    "requirements": {
      "scope": "Full IT support for 100 employees",
      "budget": "$50,000",
      "timeline": "12 months",
      "deliverables": "Monthly reports, 24/7 support"
    },
    "attachments": [],
    "status": "Published",
    "deadline": "2023-12-31T23:59:59",
    "category": "IT Services",
    "tags": ["IT", "Support", "Maintenance"],
    "responses": [],
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00",
    "published_at": "2023-01-01T00:00:00"
  }
]
```

#### Get RFP by ID

```
GET /rfps/{rfp_id}
```

Get a specific RFP by ID.

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "title": "IT Services RFP",
  "description": "Request for proposal for IT services",
  "buyer_id": "60d21b4967d0d8992e610c85",
  "requirements": {
    "scope": "Full IT support for 100 employees",
    "budget": "$50,000",
    "timeline": "12 months",
    "deliverables": "Monthly reports, 24/7 support"
  },
  "attachments": [],
  "status": "Published",
  "deadline": "2023-12-31T23:59:59",
  "category": "IT Services",
  "tags": ["IT", "Support", "Maintenance"],
  "responses": [],
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "published_at": "2023-01-01T00:00:00"
}
```

#### Update RFP

```
PUT /rfps/{rfp_id}
```

Update an RFP (Buyer only).

**Request Body:**
```json
{
  "title": "Updated IT Services RFP",
  "status": "Published"
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85",
  "title": "Updated IT Services RFP",
  "description": "Request for proposal for IT services",
  "buyer_id": "60d21b4967d0d8992e610c85",
  "requirements": {
    "scope": "Full IT support for 100 employees",
    "budget": "$50,000",
    "timeline": "12 months",
    "deliverables": "Monthly reports, 24/7 support"
  },
  "attachments": [],
  "status": "Published",
  "deadline": "2023-12-31T23:59:59",
  "category": "IT Services",
  "tags": ["IT", "Support", "Maintenance"],
  "responses": [],
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "published_at": "2023-01-01T00:00:00"
}
```

#### Submit Response to RFP

```
POST /rfps/{rfp_id}/responses
```

Submit a response to an RFP (Supplier only).

**Request Body:**
```json
{
  "content": {
    "proposal": "We offer comprehensive IT support services...",
    "pricing": "$45,000 per year",
    "timeline": "Can start immediately"
  }
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c85-60d21b4967d0d8992e610c86",
  "rfp_id": "60d21b4967d0d8992e610c85",
  "supplier_id": "60d21b4967d0d8992e610c86",
  "content": {
    "proposal": "We offer comprehensive IT support services...",
    "pricing": "$45,000 per year",
    "timeline": "Can start immediately"
  },
  "attachments": [],
  "status": "Submitted",
  "feedback": null,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Get RFP Responses

```
GET /rfps/{rfp_id}/responses
```

Get responses for an RFP. Buyers see all responses, suppliers see only their own responses.

**Response:**
```json
[
  {
    "id": "60d21b4967d0d8992e610c85-60d21b4967d0d8992e610c86",
    "rfp_id": "60d21b4967d0d8992e610c85",
    "supplier_id": "60d21b4967d0d8992e610c86",
    "content": {
      "proposal": "We offer comprehensive IT support services...",
      "pricing": "$45,000 per year",
      "timeline": "Can start immediately"
    },
    "attachments": [],
    "status": "Submitted",
    "feedback": null,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

### Document Management

#### Upload Document

```
POST /documents/upload
```

Upload a document.

**Form Data:**
- `file`: The file to upload
- `rfp_id`: RFP ID (optional)
- `response_id`: Response ID (optional)
- `is_public`: Whether the document is public (boolean, optional)

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c87",
  "filename": "f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
  "original_filename": "proposal_document.pdf",
  "file_path": "uploads/2023/01/f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
  "file_size": 1024000,
  "file_type": "pdf",
  "content_type": "application/pdf",
  "user_id": "60d21b4967d0d8992e610c86",
  "rfp_id": "60d21b4967d0d8992e610c85",
  "response_id": null,
  "is_public": false,
  "version": 1,
  "previous_versions": [],
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Get Documents

```
GET /documents
```

Get a list of documents.

**Query Parameters:**
- `rfp_id`: Filter by RFP ID (optional)
- `response_id`: Filter by response ID (optional)
- `skip`: Number of items to skip (pagination)
- `limit`: Number of items to return (pagination)

**Response:**
```json
[
  {
    "id": "60d21b4967d0d8992e610c87",
    "filename": "f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
    "original_filename": "proposal_document.pdf",
    "file_path": "uploads/2023/01/f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "content_type": "application/pdf",
    "user_id": "60d21b4967d0d8992e610c86",
    "rfp_id": "60d21b4967d0d8992e610c85",
    "response_id": null,
    "is_public": false,
    "version": 1,
    "previous_versions": [],
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

#### Get Document by ID

```
GET /documents/{document_id}
```

Get a specific document by ID.

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c87",
  "filename": "f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
  "original_filename": "proposal_document.pdf",
  "file_path": "uploads/2023/01/f7a9c4b2-1234-5678-abcd-ef1234567890.pdf",
  "file_size": 1024000,
  "file_type": "pdf",
  "content_type": "application/pdf",
  "user_id": "60d21b4967d0d8992e610c86",
  "rfp_id": "60d21b4967d0d8992e610c85",
  "response_id": null,
  "is_public": false,
  "version": 1,
  "previous_versions": [],
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Download Document

```
GET /documents/{document_id}/download
```

Download a document file.

**Response:**
The file content with appropriate Content-Type header.

### Notifications

#### Get Notifications

```
GET /notifications
```

Get a list of notifications for the current user.

**Query Parameters:**
- `is_read`: Filter by read status (boolean, optional)
- `skip`: Number of items to skip (pagination)
- `limit`: Number of items to return (pagination)

**Response:**
```json
[
  {
    "id": "60d21b4967d0d8992e610c88",
    "user_id": "60d21b4967d0d8992e610c86",
    "type": "email",
    "title": "New RFP Published",
    "message": "A new RFP has been published that matches your profile",
    "data": {
      "rfp_id": "60d21b4967d0d8992e610c85",
      "rfp_title": "IT Services RFP"
    },
    "is_read": false,
    "is_sent": true,
    "sent_at": "2023-01-01T12:00:00",
    "read_at": null,
    "created_at": "2023-01-01T12:00:00"
  }
]
```

#### Mark Notification as Read

```
PUT /notifications/{notification_id}
```

Mark a notification as read.

**Request Body:**
```json
{
  "is_read": true
}
```

**Response:**
```json
{
  "id": "60d21b4967d0d8992e610c88",
  "user_id": "60d21b4967d0d8992e610c86",
  "type": "email",
  "title": "New RFP Published",
  "message": "A new RFP has been published that matches your profile",
  "data": {
    "rfp_id": "60d21b4967d0d8992e610c85",
    "rfp_title": "IT Services RFP"
  },
  "is_read": true,
  "is_sent": true,
  "sent_at": "2023-01-01T12:00:00",
  "read_at": "2023-01-01T12:30:00",
  "created_at": "2023-01-01T12:00:00"
}
```

#### Mark All Notifications as Read

```
PUT /notifications/read-all
```

Mark all notifications as read for the current user.

**Response:**
```json
{
  "modified_count": 5
}
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON body with error details:

```json
{
  "detail": "Error message describing the problem"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. If you exceed the rate limit, you will receive a `429 Too Many Requests` response.
