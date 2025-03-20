import { Request, Response, NextFunction } from 'express';
import { ApiError } from '../middleware/errorHandler';
import logger from '../utils/logger';

/**
 * Get all users
 * @route GET /api/v1/users
 * @access Private
 */
export const getAllUsers = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // In a real application, this would query a database
    logger.info('Getting all users');
    
    const users = [
      { id: '1', name: 'John Doe', email: 'john@example.com' },
      { id: '2', name: 'Jane Smith', email: 'jane@example.com' }
    ];
    
    res.status(200).json({
      status: 'success',
      results: users.length,
      data: { users }
    });
  } catch (error: any) {
    next(new ApiError(error.message, 500));
  }
};

/**
 * Get user by ID
 * @route GET /api/v1/users/:id
 * @access Private
 */
export const getUserById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    
    // In a real application, this would query a database
    logger.info(`Getting user with ID: ${id}`);
    
    // Simulate user lookup
    if (id === '999') {
      return next(new ApiError('User not found', 404));
    }
    
    const user = {
      id,
      name: 'John Doe',
      email: 'john@example.com',
      role: 'user'
    };
    
    res.status(200).json({
      status: 'success',
      data: { user }
    });
  } catch (error: any) {
    next(new ApiError(error.message, 500));
  }
};

/**
 * Create new user
 * @route POST /api/v1/users
 * @access Admin
 */
export const createUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { name, email, password, role } = req.body;
    
    // Validate input
    if (!name || !email || !password) {
      return next(new ApiError('Please provide name, email and password', 400));
    }
    
    // In a real application, this would create a user in the database
    logger.info('Creating new user', { email });
    
    const newUser = {
      id: Math.floor(Math.random() * 1000).toString(),
      name,
      email,
      role: role || 'user'
    };
    
    res.status(201).json({
      status: 'success',
      data: { user: newUser }
    });
  } catch (error: any) {
    next(new ApiError(error.message, 500));
  }
}; 