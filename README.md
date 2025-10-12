# RFP Contract Management System

A full-stack application for managing Request for Proposal (RFP) contracts between buyers and suppliers.

## Features

- **User Management**
  - Registration with role selection (Buyer/Supplier)
  - JWT Authentication
  - Role-based access control

- **RFP Lifecycle Management**
  - Create, publish, and manage RFPs (Buyers)
  - Browse and respond to RFPs (Suppliers)
  - Review and approve/reject responses (Buyers)
  - Workflow states: Draft, Published, Response Submitted, Under Review, Approved, Rejected

- **Document Management**
  - File upload and storage
  - Document versioning
  - Secure access control

- **Notifications**
  - Email notifications for status changes
  - New RFP alerts for suppliers
  - Response alerts for buyers

- **Dashboard**
  - Role-specific dashboards
  - Real-time updates
  - Responsive design for all devices

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: MongoDB
- **Authentication**: JWT Tokens
- **Email Service**: SendGrid/Mailgun/AWS SES
- **File Storage**: Local storage (with options for AWS S3, Cloudinary)

### Frontend
- **Framework**: React with TypeScript
- **UI Library**: Material-UI
- **State Management**: React Query
- **Form Handling**: Formik with Yup validation
- **Routing**: React Router

## Quick Start

For a quick start guide, see [Quick Start Guide](docs/Quick_Start_Guide.md).

## Detailed Setup

For detailed setup instructions, see [Complete Setup Guide](docs/Complete_Setup_Guide.md).

## Demo Accounts

The application includes instructions for creating demo accounts:

- **Buyer**: buyer@test.com / password123
- **Supplier**: supplier@test.com / password123

See the [Quick Start Guide](docs/Quick_Start_Guide.md) for details on creating these accounts.

## Documentation

- [API Documentation](docs/api-docs.md)
- [Database Schema](docs/database-schema.md)
- [Productionization Guide](docs/Productionization_guide.md)
- [Project Summary](docs/Project_Summary.md)
- [AI Usage Report](docs/AI_Usage_Report.md)

## Project Structure

```
RFP_CMS/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── db/            # Database connection
│   │   ├── models/        # Data models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── templates/     # Email templates
│   │   └── utils/         # Utility functions
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React context
│   │   ├── hooks/         # Custom hooks
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   ├── package.json       # Node.js dependencies
│   └── tsconfig.json      # TypeScript configuration
├── docs/                  # Documentation
├── scripts/               # Build and deployment scripts
└── README.md              # Project documentation
```

## Security Notes

Before using in production, make sure to:

1. Replace all placeholder API keys and secrets
2. Set up proper CORS configuration
3. Configure HTTPS
4. Follow the security recommendations in the [Productionization Guide](docs/Productionization_guide.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.