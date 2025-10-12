# RFP Contract Management System - Database Schema

This document describes the MongoDB database schema used in the RFP Contract Management System.

## Collections

The system uses the following collections:

1. `users` - User accounts for buyers and suppliers
2. `rfps` - Request for Proposals
3. `documents` - Uploaded files and documents
4. `notifications` - System notifications

## Schema Definitions

### Users Collection

Stores user account information for both buyers and suppliers.

```javascript
{
  _id: ObjectId,              // Unique identifier
  email: String,              // User's email address (unique)
  username: String,           // Username (unique)
  hashed_password: String,    // Bcrypt hashed password
  first_name: String,         // User's first name (optional)
  last_name: String,          // User's last name (optional)
  role: String,               // "Buyer" or "Supplier"
  company_name: String,       // Company name (optional)
  is_active: Boolean,         // Whether the account is active
  is_verified: Boolean,       // Whether the email is verified
  created_at: DateTime,       // Account creation timestamp
  updated_at: DateTime        // Account update timestamp
}
```

#### Indexes:
- `email`: Unique index
- `username`: Unique index
- `role`: Index for filtering by role

### RFPs Collection

Stores Request for Proposal documents and their responses.

```javascript
{
  _id: ObjectId,              // Unique identifier
  title: String,              // RFP title
  description: String,        // RFP description
  buyer_id: ObjectId,         // Reference to the buyer user
  requirements: Object,       // Structured requirements data
  attachments: [String],      // Array of document IDs
  status: String,             // "Draft", "Published", "Under Review", "Completed", "Cancelled"
  deadline: DateTime,         // Submission deadline (optional)
  category: String,           // RFP category (optional)
  tags: [String],             // Array of tags
  responses: [                // Array of responses from suppliers
    {
      supplier_id: ObjectId,  // Reference to the supplier user
      content: Object,        // Structured response data
      attachments: [String],  // Array of document IDs
      status: String,         // "Submitted", "Under Review", "Approved", "Rejected"
      feedback: String,       // Feedback from buyer (optional)
      created_at: DateTime,   // Response submission timestamp
      updated_at: DateTime    // Response update timestamp
    }
  ],
  created_at: DateTime,       // RFP creation timestamp
  updated_at: DateTime,       // RFP update timestamp
  published_at: DateTime      // When the RFP was published (optional)
}
```

#### Indexes:
- `buyer_id`: Index for finding RFPs by buyer
- `status`: Index for filtering by status
- `category`: Index for filtering by category
- `tags`: Index for filtering by tags
- `deadline`: Index for sorting by deadline
- `created_at`: Index for sorting by creation date
- `published_at`: Index for sorting by publication date
- `responses.supplier_id`: Index for finding responses by supplier

### Documents Collection

Stores metadata about uploaded files.

```javascript
{
  _id: ObjectId,              // Unique identifier
  filename: String,           // Generated unique filename
  original_filename: String,  // Original uploaded filename
  file_path: String,          // Path to the file on disk or cloud storage
  file_size: Number,          // File size in bytes
  file_type: String,          // File extension (e.g., "pdf", "docx")
  content_type: String,       // MIME type
  user_id: ObjectId,          // Reference to the user who uploaded the file
  rfp_id: ObjectId,           // Reference to associated RFP (optional)
  response_id: ObjectId,      // Reference to associated response (optional)
  is_public: Boolean,         // Whether the document is publicly accessible
  version: Number,            // Document version number
  previous_versions: [ObjectId], // References to previous versions
  created_at: DateTime,       // Upload timestamp
  updated_at: DateTime        // Update timestamp
}
```

#### Indexes:
- `user_id`: Index for finding documents by user
- `rfp_id`: Index for finding documents by RFP
- `response_id`: Index for finding documents by response
- `file_type`: Index for filtering by file type
- `created_at`: Index for sorting by creation date

### Notifications Collection

Stores system notifications for users.

```javascript
{
  _id: ObjectId,              // Unique identifier
  user_id: ObjectId,          // Reference to the recipient user
  type: String,               // "email", "in_app", "sms"
  title: String,              // Notification title
  message: String,            // Notification message
  data: Object,               // Additional structured data
  is_read: Boolean,           // Whether the notification has been read
  is_sent: Boolean,           // Whether the notification has been sent
  sent_at: DateTime,          // When the notification was sent (optional)
  read_at: DateTime,          // When the notification was read (optional)
  created_at: DateTime        // Notification creation timestamp
}
```

#### Indexes:
- `user_id`: Index for finding notifications by user
- `is_read`: Index for filtering by read status
- `created_at`: Index for sorting by creation date
- `user_id, is_read`: Compound index for finding unread notifications for a user

## Relationships

The following diagram illustrates the relationships between collections:

```
Users
  ↑
  | (buyer_id)
  |
RFPs ----→ Documents
  |         ↑
  |         | (document_id)
  |         |
  ↓         |
Responses ---
  |
  | (supplier_id)
  ↓
Users

Notifications
  |
  | (user_id)
  ↓
Users
```

## Data Validation

MongoDB schema validation is used to ensure data integrity:

- Required fields are enforced
- String fields have maximum lengths
- Enum fields are restricted to valid values
- Date fields are validated as proper dates
- Numeric fields have appropriate ranges

## Indexing Strategy

Indexes are created for:
- All fields used in query filters
- Fields used for sorting
- Fields used in aggregation operations
- Fields used in joins between collections

## Data Migration

For future schema changes, migration scripts will be provided in the `scripts/migrations` directory.

## Backup Strategy

Regular backups of the MongoDB database should be configured:
- Daily full backups
- Hourly incremental backups
- Retention period of 30 days

## Performance Considerations

- Use appropriate indexes for common queries
- Limit the size of embedded arrays (like responses in RFPs)
- Consider moving large embedded documents to separate collections if they grow too large
- Use projection to limit the fields returned in queries
- Use pagination for large result sets
