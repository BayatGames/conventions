import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';
import { ApiError } from 'shared/types';

class HttpException extends Error {
  status: number;
  message: string;
  errors?: Record<string, string[]>;

  constructor(status: number, message: string, errors?: Record<string, string[]>) {
    super(message);
    this.status = status;
    this.message = message;
    this.errors = errors;
  }
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  let status = 500;
  let message = 'Internal Server Error';
  let errors: Record<string, string[]> | undefined;

  // Handle known error types
  if (err instanceof HttpException) {
    status = err.status;
    message = err.message;
    errors = err.errors;
  }

  // Log the error
  logger.error(`${status} - ${message} - ${req.originalUrl} - ${req.method}`);

  if (err.stack) {
    logger.error(err.stack);
  }

  // Send error response
  const errorResponse: ApiError = {
    message,
    status,
  };

  if (errors) {
    errorResponse.errors = errors;
  }

  return res.status(status).json(errorResponse);
};

export { HttpException }; 