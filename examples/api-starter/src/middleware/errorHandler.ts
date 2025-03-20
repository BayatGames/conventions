import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';
import { config } from '../config';

// Custom error class for API errors
export class ApiError extends Error {
  statusCode: number;
  isOperational: boolean;

  constructor(message: string, statusCode: number, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Dev error response
const sendErrorDev = (err: ApiError, res: Response) => {
  res.status(err.statusCode).json({
    status: 'error',
    message: err.message,
    error: err,
    stack: err.stack,
  });
};

// Production error response
const sendErrorProd = (err: ApiError, res: Response) => {
  // Operational, trusted error: send message to client
  if (err.isOperational) {
    res.status(err.statusCode).json({
      status: 'error',
      message: err.message,
    });
  } else {
    // Programming or other unknown error: don't leak error details
    logger.error('Unexpected error', { error: err.message, stack: err.stack });
    res.status(500).json({
      status: 'error',
      message: 'Something went wrong',
    });
  }
};

// Global error handler middleware
export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const apiError = err instanceof ApiError
    ? err
    : new ApiError(err.message || 'Internal Server Error', 500, false);
  
  logger.error(`${apiError.statusCode} - ${apiError.message} - ${req.originalUrl} - ${req.method} - ${req.ip}`);

  if (config.env === 'development') {
    sendErrorDev(apiError, res);
  } else {
    sendErrorProd(apiError, res);
  }
}; 