# User Service

This service handles user management functionality within the microservices architecture.

## Features

- User registration and authentication
- JWT-based authorization
- User profile management
- Role-based access control
- Event emission for user-related activities

## Tech Stack

- Node.js with Express
- TypeScript
- MongoDB with Mongoose
- Kafka for event streaming
- JWT for authentication
- Docker for containerization

## Getting Started

### Prerequisites

- Node.js (v16+)
- Docker and Docker Compose
- MongoDB (or use the Docker Compose setup)

### Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies:

```bash
npm install
```

### Running locally

```bash
# Development mode with hot reloading
npm run dev

# Production mode
npm run build
npm start
```

### Running with Docker

```bash
docker build -t user-service .
docker run -p 3001:3001 --env-file .env user-service
```

## API Documentation

Once the service is running, Swagger documentation can be accessed at:

```
http://localhost:3001/api-docs
```

## Testing

```bash
# Run tests
npm test

# Run linting
npm run lint
```

## Event Publishing

This service publishes the following events to Kafka:

- `USER_CREATED`: When a new user is registered
- `USER_UPDATED`: When a user profile is updated
- `USER_DELETED`: When a user is deleted

These events can be consumed by other services that need to react to user changes. 