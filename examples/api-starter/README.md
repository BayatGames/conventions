<!--
Document: API Starter Example
Version: 1.0.0
Last Updated: 2023-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2023-03-20: Initial version
-->

# Bayat API Starter

This repository serves as a reference implementation of Bayat's API development conventions. It provides a production-ready starting point for building RESTful APIs using Node.js, Express, and TypeScript.

## Conventions Demonstrated

This example demonstrates the following Bayat conventions:

- **API Design**: RESTful endpoint structure, versioning, and error handling
- **Project Structure**: Modular organization for scalability
- **Type Safety**: TypeScript implementation with proper typing
- **Testing**: Unit, integration, and API testing patterns
- **Documentation**: OpenAPI/Swagger documentation
- **Security**: Authentication, authorization, and data validation
- **Logging**: Structured logging patterns
- **Configuration**: Environment-based configuration management

## Getting Started

```bash
# Clone the repository
git clone https://github.com/bayat/examples/api-starter

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
```

## Project Structure

```plaintext
.
├── src/
│   ├── config/         # Configuration management
│   ├── controllers/    # Route handlers
│   ├── middleware/     # Express middleware
│   ├── models/         # Data models
│   ├── routes/         # API routes
│   ├── services/       # Business logic
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── app.ts          # Express application setup
│   └── server.ts       # Server entry point
├── tests/              # Test files
├── docs/               # Documentation
├── .env.example        # Example environment variables
├── tsconfig.json       # TypeScript configuration
├── package.json        # Dependencies and scripts
└── README.md           # Project documentation
```

## Key Features

- **Express Router**: Organized routing with versioning
- **Middleware Pipeline**: Authentication, logging, error handling
- **Environment Config**: Development, test, production profiles
- **Structured Error Handling**: Consistent error responses
- **Request Validation**: Schema validation with Joi/Zod
- **Database Integration**: Example with PostgreSQL
- **Logging**: Structured JSON logging
- **Testing**: Jest configuration with examples
- **Documentation**: OpenAPI spec and Swagger UI
- **Containerization**: Docker setup for deployment

## Contribution Guidelines

Please refer to the main [Contribution Guidelines](../../CONTRIBUTING.md) for information on contributing to this example.
