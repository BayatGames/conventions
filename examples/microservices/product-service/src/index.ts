import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import { Kafka } from 'kafkajs';
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import pino from 'pino-http';
import dotenv from 'dotenv';

import productRoutes from './routes/productRoutes';

// Load environment variables
dotenv.config();

// Initialize express app
const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Setup logger
const logger = pino();
app.use(logger);

// Serve static files from uploads directory
app.use('/uploads', express.static('uploads'));

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/product-service')
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err);
    process.exit(1);
  });

// Initialize Kafka Producer
const kafka = new Kafka({
  clientId: 'product-service',
  brokers: (process.env.KAFKA_BROKERS || 'localhost:9092').split(','),
});

const producer = kafka.producer();

// Connect Kafka producer
producer.connect()
  .then(() => {
    console.log('Kafka producer connected');
    // Store the producer in app.locals for use in controllers
    app.locals.kafkaProducer = producer;
  })
  .catch((err) => {
    console.error('Kafka producer connection error:', err);
  });

// Swagger documentation setup
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Product Service API',
      version: '1.0.0',
      description: 'API documentation for the Product Service',
    },
    servers: [
      {
        url: `http://localhost:${PORT}`,
        description: 'Development server',
      },
    ],
  },
  apis: ['./src/routes/*.ts', './src/models/*.ts'],
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// API Routes
app.use('/api/products', productRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Start the server
const server = app.listen(PORT, () => {
  console.log(`Product service running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  
  // Close server
  server.close(async () => {
    console.log('HTTP server closed');
    
    // Disconnect Kafka producer
    await producer.disconnect();
    console.log('Kafka producer disconnected');
    
    // Disconnect from MongoDB
    await mongoose.disconnect();
    console.log('MongoDB disconnected');
    
    process.exit(0);
  });
});

export default app; 