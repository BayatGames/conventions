# Order Service

This service handles order management functionality within the microservices architecture.

## Features

- Order creation and management
- Order status updates
- Integration with user service for customer information
- Event emission for order-related activities

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
docker build -t order-service .
docker run -p 3002:3002 --env-file .env order-service
```

## API Documentation

Once the service is running, Swagger documentation can be accessed at:

```
http://localhost:3002/api-docs
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

- `ORDER_CREATED`: When a new order is created
- `ORDER_UPDATED`: When an order is updated
- `ORDER_SHIPPED`: When an order is shipped
- `ORDER_DELIVERED`: When an order is delivered
- `ORDER_CANCELLED`: When an order is cancelled

These events can be consumed by other services (like notification service) that need to react to order changes. 