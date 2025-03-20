# Notification Service

This service handles notification delivery functionality within the microservices architecture.

## Features

- Multi-channel notifications (Email, SMS, Push)
- Event-driven architecture using Kafka
- Notification templates for various events
- Delivery status tracking

## Tech Stack

- Node.js with Express
- TypeScript
- MongoDB with Mongoose
- Kafka for event streaming
- Nodemailer for email delivery
- Twilio for SMS delivery
- Docker for containerization

## Getting Started

### Prerequisites

- Node.js (v16+)
- Docker and Docker Compose
- MongoDB (or use the Docker Compose setup)
- SMTP server for email delivery
- Twilio account for SMS delivery

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
docker build -t notification-service .
docker run -p 3003:3003 --env-file .env notification-service
```

## API Documentation

Once the service is running, Swagger documentation can be accessed at:

```
http://localhost:3003/api-docs
```

## Testing

```bash
# Run tests
npm test

# Run linting
npm run lint
```

## Event Consumption

This service consumes the following events from Kafka:

### User Events
- `USER_CREATED`: Sends welcome emails to new users
- `USER_UPDATED`: Notifies users about profile changes

### Order Events
- `ORDER_CREATED`: Sends order confirmation to customers
- `ORDER_UPDATED`: Notifies customers about order updates
- `ORDER_SHIPPED`: Sends shipping notifications with tracking info
- `ORDER_DELIVERED`: Sends delivery confirmation
- `ORDER_CANCELLED`: Notifies customers about order cancellations

## Notification Channels

### Email
Uses Nodemailer to send HTML emails through configured SMTP server.

### SMS
Uses Twilio API to send text messages to user phone numbers.

### Push (Future)
Framework is in place to support push notifications in the future. 