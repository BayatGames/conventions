<!--
Document: Microservices Architecture Demo
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Microservices Architecture Demo

This project demonstrates a modern microservices architecture with multiple services communicating through an API Gateway and event-driven patterns.

## Architecture Overview

![Microservices Architecture](./architecture.png)

### Components

- **API Gateway (Kong)**: Routes client requests to appropriate services
- **User Service**: Manages user accounts and authentication
- **Order Service**: Handles order creation and management
- **Notification Service**: Sends notifications via email, SMS, etc.
- **Kafka**: Message broker for event-driven communication between services
- **MongoDB**: Database for each service (separate database per service)

## Services

### User Service

Responsible for user management, authentication, and authorization.

- **Endpoints**:
  - User registration and login
  - User profile management
  - Access control

- **Events Published**:
  - `USER_CREATED`: When a new user is registered
  - `USER_UPDATED`: When a user profile is updated
  - `USER_DELETED`: When a user is deleted

### Order Service

Manages the lifecycle of orders in the system.

- **Endpoints**:
  - Create, read, update, delete orders
  - Order status management
  - Order history

- **Events Published**:
  - `ORDER_CREATED`: When a new order is created
  - `ORDER_UPDATED`: When an order is updated
  - `ORDER_SHIPPED`: When an order is shipped
  - `ORDER_DELIVERED`: When an order is delivered
  - `ORDER_CANCELLED`: When an order is cancelled

### Notification Service

Handles sending notifications to users through various channels.

- **Channels**:
  - Email (via Nodemailer)
  - SMS (via Twilio)
  - Push notifications (future)

- **Events Consumed**:
  - User events: Welcome emails, profile updates
  - Order events: Order confirmations, shipping updates, etc.

## Technology Stack

- **Backend**: Node.js, Express, TypeScript
- **Databases**: MongoDB
- **Message Broker**: Apache Kafka
- **API Gateway**: Kong
- **Authentication**: JWT
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker
- **Container Orchestration**: Docker Compose (Kubernetes-ready)
- **Logging**: Pino

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)

### Running the Application

1. Clone the repository
2. Create `.env` files in each service directory based on the provided `.env.example` files
3. Start the application using Docker Compose:

```bash
docker-compose up
```

4. Access the services:
   - API Gateway: http://localhost:8000
   - User Service: http://localhost:3001
   - Order Service: http://localhost:3002
   - Notification Service: http://localhost:3003
   - Kafka UI: http://localhost:8080
   - MongoDB Express (DB Admin): http://localhost:8081

## API Documentation

Each service provides Swagger documentation available at `/api-docs` endpoint.

- User Service API Docs: http://localhost:3001/api-docs
- Order Service API Docs: http://localhost:3002/api-docs
- Notification Service API Docs: http://localhost:3003/api-docs

## Development

### Local Development

Each service can be run independently for development:

```bash
cd user-service
npm install
npm run dev
```

### Testing

```bash
npm test
```

## Design Patterns and Principles

- **Service Discovery**: Services register with the API Gateway
- **Circuit Breaker**: Preventing cascading failures
- **Event Sourcing**: Using Kafka for event-driven architecture
- **CQRS**: Separation of read and write operations
- **Database per Service**: Each service has its own database
- **API Gateway**: Single entry point for all client requests
- **JWT Authentication**: Secure, stateless authentication

## Monitoring and Observability

- **Health Checks**: Each service provides a `/health` endpoint
- **Logging**: Structured logging with Pino
- **Metrics**: Prometheus-compatible metrics (future)
- **Tracing**: Distributed tracing with OpenTelemetry (future)

## Security Features

- **Rate Limiting**: Configured at the API Gateway level
- **JWT Authentication**: Secure token-based authentication
- **CORS**: Configured for web client access
- **Input Validation**: Request validation using express-validator

## Future Enhancements

- Kubernetes deployment configuration
- Centralized configuration server
- Advanced monitoring with Prometheus and Grafana
- Distributed tracing with Jaeger
- CI/CD pipeline for automated testing and deployment

## Project Structure

```plaintext
microservices/
├── api-gateway/         # Kong gateway configuration
├── user-service/        # Node.js service for user management
├── order-service/       # Go service for order processing
├── notification-service/ # Node.js service for notifications
├── shared/              # Shared libraries and types
├── kubernetes/          # Kubernetes manifests
├── docker-compose.yml   # Local development environment
└── README.md            # This file
```

## Contributing

Please see the [Contributing Guide](../../CONTRIBUTING.md) for information on how to contribute to this example.
