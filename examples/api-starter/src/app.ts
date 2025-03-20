import express, { Application, Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import cors from 'cors';
import swaggerUi from 'swagger-ui-express';
import fs from 'fs';
import path from 'path';

import { config } from './config';
import { logStream } from './utils/logger';
import apiRouter from './routes';
import { errorHandler } from './middleware/errorHandler';

// Initialize express app
const app: Application = express();

// Apply security middleware
app.use(helmet());

// Set up CORS
app.use(cors({
  origin: config.server.corsOrigin,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Request parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use(morgan(config.logging.format, { stream: logStream }));

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'success',
    message: 'API is healthy',
    timestamp: new Date().toISOString(),
    environment: config.env,
    version: process.env.npm_package_version || '1.0.0'
  });
});

// API routes
app.use(`/api/${config.apiVersion}`, apiRouter);

// Swagger documentation
const swaggerFile = path.resolve(__dirname, '../docs/swagger.json');
if (fs.existsSync(swaggerFile)) {
  app.use(`/api/${config.apiVersion}/docs`, swaggerUi.serve, swaggerUi.setup(require(swaggerFile)));
}

// 404 handler
app.use('*', (req: Request, res: Response) => {
  res.status(404).json({
    status: 'error',
    message: `Can't find ${req.originalUrl} on this server`
  });
});

// Global error handler
app.use(errorHandler);

export default app; 