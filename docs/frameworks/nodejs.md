<!--
Document: Node.js Development Conventions
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Node.js Development Conventions

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Coding Style](#coding-style)
4. [API Design](#api-design)
5. [Database Integration](#database-integration)
6. [Authentication and Authorization](#authentication-and-authorization)
7. [Error Handling](#error-handling)
8. [Logging](#logging)
9. [Testing](#testing)
10. [Performance Optimization](#performance-optimization)
11. [Security Best Practices](#security-best-practices)
12. [Environment Configuration](#environment-configuration)
13. [Documentation](#documentation)
14. [Deployment](#deployment)
15. [Monitoring](#monitoring)
16. [Containerization](#containerization)
17. [Microservices](#microservices)
18. [Version Control](#version-control)

## Introduction

This document outlines the standard conventions and best practices for Node.js application development at Bayat. These guidelines aim to ensure consistency, maintainability, and scalability across all Node.js projects.

## Project Structure

### Folder Organization

```
project-root/
├── src/                    # Application source code
│   ├── api/                # API routes and controllers
│   │   ├── controllers/    # Request handlers
│   │   ├── middlewares/    # Express middlewares
│   │   ├── routes/         # Route definitions
│   │   └── validators/     # Request validation
│   ├── config/             # Configuration files
│   ├── db/                 # Database setup and migrations
│   │   ├── migrations/     # Database migrations
│   │   ├── models/         # Database models
│   │   └── seeds/          # Seed data
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── workers/            # Background workers
│   └── app.js              # Application entry point
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   ├── e2e/                # End-to-end tests
│   └── fixtures/           # Test fixtures
├── scripts/                # Utility scripts
├── logs/                   # Application logs
├── docs/                   # Documentation
├── .env.example            # Example environment variables
├── .eslintrc.js            # ESLint configuration
├── .prettierrc             # Prettier configuration
├── jest.config.js          # Jest configuration
├── nodemon.json            # Nodemon configuration
├── package.json            # Dependencies and scripts
└── README.md               # Project documentation
```

### Module Organization

- Group related functionality into modules
- Each module should have a clear responsibility
- Use index.js files to expose public interfaces
- Keep circular dependencies to a minimum

## Coding Style

### JavaScript/TypeScript Standards

- Follow the Airbnb JavaScript Style Guide
- Use ESLint and Prettier for code formatting
- Prefer const over let, and avoid var
- Use async/await over callbacks and Promise chains
- Use destructuring for cleaner code
- Prefer template literals over string concatenation

```javascript
// Good
const { firstName, lastName } = user;
const fullName = `${firstName} ${lastName}`;

// Avoid
const firstName = user.firstName;
const lastName = user.lastName;
const fullName = firstName + ' ' + lastName;
```

### Naming Conventions

- Use camelCase for variables, functions, and methods
- Use PascalCase for classes and constructor functions
- Use UPPER_SNAKE_CASE for constants
- Use descriptive names that reveal intent

```javascript
// Good
const userService = new UserService();
const MAX_LOGIN_ATTEMPTS = 5;

function calculateTotalPrice(items) {
  // Implementation
}

class AuthenticationManager {
  // Implementation
}
```

### TypeScript Usage (when applicable)

- Define interfaces for all data structures
- Use type annotations for function parameters and return types
- Leverage union types and generics for flexibility
- Avoid using `any` type when possible
- Use enums for sets of related constants

```typescript
interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  createdAt: Date;
}

enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

function getUserById(id: string): Promise<User | null> {
  // Implementation
}
```

## API Design

### RESTful API Guidelines

- Use nouns, not verbs, in endpoint paths
- Use plural nouns for collections
- Use HTTP methods appropriately (GET, POST, PUT, DELETE)
- Use nested routes for representing relationships
- Implement proper status codes
- Version your APIs (e.g., /api/v1/users)

```javascript
// Good API routes
router.get('/users', userController.listUsers);
router.get('/users/:id', userController.getUserById);
router.post('/users', userController.createUser);
router.put('/users/:id', userController.updateUser);
router.delete('/users/:id', userController.deleteUser);
router.get('/users/:userId/orders', orderController.getUserOrders);
```

### Request Validation

- Validate all input data
- Use a validation library like Joi or express-validator
- Return clear validation error messages
- Sanitize user input to prevent injection attacks

```javascript
// Using Joi for validation
const createUserSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  firstName: Joi.string().required(),
  lastName: Joi.string().required(),
  role: Joi.string().valid('admin', 'user', 'guest').default('user')
});

router.post('/users', validate(createUserSchema), userController.createUser);
```

### Response Formatting

- Use a consistent response format
- Include status, data, and error fields
- Implement pagination for list endpoints
- Use HATEOAS principles for discoverability

```javascript
// Example response format
{
  "status": "success",
  "data": {
    "user": {
      "id": "123",
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe"
    }
  },
  "links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders"
  }
}
```

## Database Integration

### ORM/ODM Usage

- Use Sequelize for SQL databases
- Use Mongoose for MongoDB
- Define clear models with validation
- Implement database migrations
- Use transactions for operations that modify multiple records

```javascript
// Mongoose model example
const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  role: {
    type: String,
    enum: ['admin', 'user', 'guest'],
    default: 'user'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model('User', userSchema);
```

### Query Optimization

- Use indexes for frequently queried fields
- Select only needed fields
- Implement pagination for large result sets
- Use query caching when appropriate
- Monitor and optimize slow queries

```javascript
// Optimized query example
const users = await User.find({ role: 'user' })
  .select('firstName lastName email')
  .sort({ createdAt: -1 })
  .skip((page - 1) * limit)
  .limit(limit)
  .cache({ key: `users_page_${page}` });
```

### Database Connection Management

- Implement connection pooling
- Handle connection errors gracefully
- Use environment variables for database credentials
- Implement retry logic for transient failures
- Close connections properly when the application shuts down

## Authentication and Authorization

### Authentication Strategies

- Use JWT for stateless authentication
- Implement refresh token rotation
- Store passwords using strong hashing algorithms (bcrypt)
- Support multi-factor authentication for sensitive operations
- Implement proper session management if using sessions

```javascript
// JWT authentication example
const generateTokens = (user) => {
  const accessToken = jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_ACCESS_SECRET,
    { expiresIn: '15m' }
  );
  
  const refreshToken = jwt.sign(
    { id: user.id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );
  
  return { accessToken, refreshToken };
};
```

### Authorization

- Implement role-based access control (RBAC)
- Use middleware for authorization checks
- Apply the principle of least privilege
- Document permission requirements for each endpoint
- Implement attribute-based access control for complex scenarios

```javascript
// Authorization middleware
const authorize = (requiredRole) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        status: 'error',
        message: 'Unauthorized'
      });
    }
    
    if (requiredRole && req.user.role !== requiredRole) {
      return res.status(403).json({
        status: 'error',
        message: 'Forbidden'
      });
    }
    
    next();
  };
};

// Usage
router.get('/admin/stats', authenticate, authorize('admin'), adminController.getStats);
```

## Error Handling

### Error Types

- Define custom error classes
- Distinguish between operational errors and programmer errors
- Use appropriate HTTP status codes
- Include error codes for client-side handling

```javascript
// Custom error classes
class AppError extends Error {
  constructor(message, statusCode, errorCode) {
    super(message);
    this.statusCode = statusCode;
    this.errorCode = errorCode;
    this.isOperational = true;
    
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'RESOURCE_NOT_FOUND');
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}
```

### Global Error Handling

- Implement a centralized error handler
- Log all errors appropriately
- Return user-friendly error messages
- Include detailed error information in development
- Handle uncaught exceptions and unhandled rejections

```javascript
// Global error handler middleware
const errorHandler = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  
  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    requestId: req.id,
    path: req.path
  });
  
  // Response for client
  const response = {
    status: 'error',
    message: err.isOperational ? err.message : 'Something went wrong',
  };
  
  if (process.env.NODE_ENV === 'development') {
    response.stack = err.stack;
    response.errorCode = err.errorCode;
  }
  
  res.status(err.statusCode).json(response);
};

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  logger.error({
    message: 'UNCAUGHT EXCEPTION',
    error: err.message,
    stack: err.stack
  });
  
  // Graceful shutdown
  process.exit(1);
});
```

## Logging

### Logging Levels

- Use appropriate logging levels (error, warn, info, debug)
- Configure different log destinations based on environment
- Include contextual information in logs
- Implement request ID tracking across services

```javascript
// Winston logger configuration
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});
```

### Request Logging

- Log incoming requests and responses
- Include request duration
- Mask sensitive data in logs
- Use a request logger middleware

```javascript
// Request logger middleware
const requestLogger = (req, res, next) => {
  const requestId = uuid.v4();
  req.id = requestId;
  
  // Log request
  logger.info({
    message: 'Incoming request',
    method: req.method,
    path: req.path,
    requestId,
    ip: req.ip
  });
  
  // Track response time
  const start = Date.now();
  
  // Log response
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      message: 'Request completed',
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      requestId
    });
  });
  
  next();
};
```

## Testing

### Test Types

1. **Unit Tests**: Test individual functions and components
2. **Integration Tests**: Test interactions between components
3. **API Tests**: Test API endpoints
4. **End-to-End Tests**: Test complete workflows

### Testing Framework

- Use Jest as the test runner
- Use Supertest for API testing
- Implement test fixtures and factories
- Use mocks and stubs for external dependencies

```javascript
// Example unit test
describe('User Service', () => {
  describe('createUser', () => {
    it('should create a new user', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'Test',
        lastName: 'User'
      };
      
      const mockUserRepository = {
        create: jest.fn().mockResolvedValue({
          id: '123',
          ...userData,
          password: 'hashed_password'
        })
      };
      
      const userService = new UserService(mockUserRepository);
      
      // Act
      const result = await userService.createUser(userData);
      
      // Assert
      expect(mockUserRepository.create).toHaveBeenCalledWith({
        ...userData,
        password: expect.any(String) // Hashed password
      });
      
      expect(result).toEqual({
        id: '123',
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName
      });
    });
  });
});
```

### Test Coverage

- Aim for high test coverage (>80%)
- Focus on testing business logic
- Implement CI/CD pipeline for automated testing
- Generate test coverage reports

## Performance Optimization

### Code Optimization

- Use asynchronous operations
- Implement caching for expensive operations
- Optimize database queries
- Use streams for handling large files
- Implement pagination for large data sets

```javascript
// Caching example with Redis
const getUser = async (userId) => {
  // Try to get from cache
  const cachedUser = await redisClient.get(`user:${userId}`);
  if (cachedUser) {
    return JSON.parse(cachedUser);
  }
  
  // Get from database
  const user = await User.findById(userId);
  if (!user) {
    throw new NotFoundError('User');
  }
  
  // Cache result
  await redisClient.set(
    `user:${userId}`,
    JSON.stringify(user),
    'EX',
    3600 // Expire in 1 hour
  );
  
  return user;
};
```

### Server Optimization

- Use clustering to utilize multiple CPU cores
- Implement proper load balancing
- Use a reverse proxy (Nginx) in production
- Configure appropriate timeouts
- Implement rate limiting

```javascript
// Clustering example
const cluster = require('cluster');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  
  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    // Replace the dead worker
    cluster.fork();
  });
} else {
  // Workers can share any TCP connection
  // In this case, it's an HTTP server
  require('./app');
}
```

## Security Best Practices

### Input Validation

- Validate and sanitize all user input
- Implement content security policy
- Use parameterized queries to prevent SQL injection
- Validate file uploads (type, size, content)

### Authentication Security

- Implement proper password policies
- Use secure cookies with appropriate flags
- Implement rate limiting for authentication attempts
- Use HTTPS for all communications
- Implement proper CORS configuration

```javascript
// CORS configuration
const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS.split(','),
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400 // 24 hours
};

app.use(cors(corsOptions));
```

### Dependency Security

- Regularly update dependencies
- Use npm audit to check for vulnerabilities
- Implement a security policy
- Use a dependency scanning tool in CI/CD pipeline

## Environment Configuration

### Environment Variables

- Use dotenv for local development
- Never commit sensitive information to version control
- Use different configurations for different environments
- Validate required environment variables on startup

```javascript
// Environment configuration
require('dotenv').config();

const requiredEnvVars = [
  'NODE_ENV',
  'PORT',
  'DATABASE_URL',
  'JWT_SECRET'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.error(`Error: Environment variable ${envVar} is required`);
    process.exit(1);
  }
}

const config = {
  env: process.env.NODE_ENV,
  port: process.env.PORT,
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  logLevel: process.env.LOG_LEVEL || 'info'
};

module.exports = config;
```

### Configuration Management

- Use a hierarchical configuration system
- Implement feature flags
- Use secrets management for sensitive information
- Document all configuration options

## Documentation

### Code Documentation

- Use JSDoc for documenting functions and classes
- Document complex algorithms and business logic
- Keep documentation up-to-date with code changes
- Generate API documentation from code comments

```javascript
/**
 * Creates a new user in the system
 * 
 * @param {Object} userData - The user data
 * @param {string} userData.email - User's email address
 * @param {string} userData.password - User's password (will be hashed)
 * @param {string} userData.firstName - User's first name
 * @param {string} userData.lastName - User's last name
 * @param {string} [userData.role='user'] - User's role
 * @returns {Promise<Object>} The created user (without password)
 * @throws {ValidationError} If validation fails
 * @throws {DuplicateError} If email already exists
 */
async function createUser(userData) {
  // Implementation
}
```

### API Documentation

- Use Swagger/OpenAPI for API documentation
- Include request/response examples
- Document authentication requirements
- Keep documentation up-to-date with API changes

## Deployment

### Deployment Strategies

- Implement CI/CD pipelines
- Use environment-specific configurations
- Implement blue-green deployments
- Use infrastructure as code

### Production Readiness

- Implement health checks
- Configure proper logging
- Set up monitoring and alerting
- Implement backup and recovery procedures
- Document deployment and rollback procedures

```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  const healthcheck = {
    uptime: process.uptime(),
    message: 'OK',
    timestamp: Date.now()
  };
  
  try {
    // Check database connection
    if (!mongoose.connection.readyState) {
      healthcheck.message = 'Database connection error';
      return res.status(503).json(healthcheck);
    }
    
    // Check other dependencies
    
    res.status(200).json(healthcheck);
  } catch (error) {
    healthcheck.message = error.message;
    res.status(503).json(healthcheck);
  }
});
```

## Monitoring

### Application Monitoring

- Implement application metrics collection
- Monitor response times and error rates
- Set up alerts for critical issues
- Use distributed tracing for microservices

```javascript
// Prometheus metrics example
const promClient = require('prom-client');
const collectDefaultMetrics = promClient.collectDefaultMetrics;

// Collect default metrics
collectDefaultMetrics({ timeout: 5000 });

// Custom metrics
const httpRequestDurationMicroseconds = new promClient.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});
```

### Performance Monitoring

- Monitor CPU and memory usage
- Track database performance
- Implement log aggregation
- Use APM tools for detailed performance insights

## Containerization

### Docker Configuration

- Create optimized Dockerfiles
- Use multi-stage builds
- Implement proper caching
- Use environment variables for configuration
- Minimize container size

```dockerfile
# Example Dockerfile
FROM node:16-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Production image
FROM node:16-alpine

WORKDIR /app

# Copy from builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/src ./src
COPY --from=builder /app/package.json ./

# Set environment variables
ENV NODE_ENV=production

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Run the application
CMD ["node", "src/app.js"]
```

### Container Orchestration

- Use Docker Compose for local development
- Implement Kubernetes for production
- Define resource limits
- Implement proper scaling policies
- Use secrets management

## Microservices

### Service Design

- Define clear service boundaries
- Implement proper inter-service communication
- Use API gateways for client-facing services
- Implement service discovery
- Design for failure

### Communication Patterns

- Use REST for synchronous communication
- Implement message queues for asynchronous communication
- Use event-driven architecture when appropriate
- Implement circuit breakers for resilience

```javascript
// Message queue example with RabbitMQ
const amqp = require('amqplib');

async function publishEvent(exchange, routingKey, message) {
  const connection = await amqp.connect(process.env.RABBITMQ_URL);
  const channel = await connection.createChannel();
  
  await channel.assertExchange(exchange, 'topic', { durable: true });
  
  channel.publish(
    exchange,
    routingKey,
    Buffer.from(JSON.stringify(message)),
    { persistent: true }
  );
  
  await channel.close();
  await connection.close();
}

// Usage
await publishEvent(
  'user-events',
  'user.created',
  { id: user.id, email: user.email }
);
```

## Version Control

### Git Workflow

- Follow the Bayat Git Flow
- Write meaningful commit messages
- Use feature branches for development
- Implement code reviews via pull requests
- Keep branches up-to-date with the main branch

### Release Management

- Use semantic versioning
- Create release branches
- Tag releases
- Maintain a changelog
- Automate the release process 