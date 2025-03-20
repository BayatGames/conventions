# Product Service

This microservice is responsible for product management within the e-commerce platform. It provides APIs for creating, retrieving, updating, and deleting products, as well as handling product image uploads and inventory management.

## Features

- CRUD operations for products
- Product image upload
- Inventory management
- Product categorization
- Search and filtering functionality
- Admin-only actions for product management
- Event-driven communication with other services via Kafka

## Tech Stack

- Node.js
- TypeScript
- Express.js
- MongoDB with Mongoose
- Kafka for event-driven communication
- JWT for authentication
- Multer for file uploads
- Swagger for API documentation

## API Endpoints

- `GET /api/products` - Get all products (with pagination and filtering)
- `GET /api/products/:id` - Get a product by ID
- `POST /api/products` - Create a new product (admin only)
- `PUT /api/products/:id` - Update a product (admin only)
- `DELETE /api/products/:id` - Delete a product (soft delete, admin only)
- `PATCH /api/products/:id/inventory` - Update product inventory (admin only)

## Events Published

- `PRODUCT_CREATED` - When a new product is created
- `PRODUCT_UPDATED` - When a product is updated
- `PRODUCT_DELETED` - When a product is deleted (soft delete)
- `PRODUCT_INVENTORY_UPDATED` - When a product's inventory is updated

## Environment Variables

```
NODE_ENV=development
PORT=3004
MONGODB_URI=mongodb://localhost:27017/product-service
JWT_SECRET=your_jwt_secret_key_here
KAFKA_BROKERS=localhost:9092
KAFKA_CLIENT_ID=product-service
KAFKA_GROUP_ID=product-service-group
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5000000
LOG_LEVEL=info
CORS_ORIGIN=*
```

## Getting Started

### Prerequisites

- Node.js (>=14.x)
- MongoDB
- Kafka

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file with the required environment variables
4. Run the development server:
   ```
   npm run dev
   ```

### Building for Production

```
npm run build
```

### Running in Production

```
npm start
```

## Docker

Build the Docker image:

```
docker build -t product-service .
```

Run the container:

```
docker run -p 3004:3004 --env-file .env product-service
```

## API Documentation

The API documentation is available at `/api-docs` when the service is running. 