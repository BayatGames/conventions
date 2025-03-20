import { Request, Response, NextFunction } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { validationResult } from 'express-validator';
import { prisma } from '../index';
import { HttpException } from '../middlewares/errorHandler';
import { User, LoginCredentials, RegisterCredentials } from 'shared/types';

// Register a new user
export const register = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      throw new HttpException(400, 'Validation error', 
        errors.array().reduce((acc: Record<string, string[]>, error: any) => {
          const key = error.param;
          if (!acc[key]) acc[key] = [];
          acc[key].push(error.msg);
          return acc;
        }, {})
      );
    }
    
    const { email, password, firstName, lastName } = req.body as RegisterCredentials;
    
    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });
    
    if (existingUser) {
      throw new HttpException(400, 'User with this email already exists');
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const newUser = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        firstName,
        lastName,
      },
    });
    
    // Generate JWT
    const token = jwt.sign(
      { userId: newUser.id },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );
    
    // Return user data and token
    res.status(201).json({
      user: {
        id: newUser.id,
        email: newUser.email,
        firstName: newUser.firstName,
        lastName: newUser.lastName,
        role: newUser.role,
        createdAt: newUser.createdAt.toISOString(),
        updatedAt: newUser.updatedAt.toISOString(),
      },
      token,
    });
  } catch (error) {
    next(error);
  }
};

// Login a user
export const login = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      throw new HttpException(400, 'Validation error',
        errors.array().reduce((acc: Record<string, string[]>, error: any) => {
          const key = error.param;
          if (!acc[key]) acc[key] = [];
          acc[key].push(error.msg);
          return acc;
        }, {})
      );
    }
    
    const { email, password } = req.body as LoginCredentials;
    
    // Check if user exists
    const user = await prisma.user.findUnique({
      where: { email },
    });
    
    if (!user) {
      throw new HttpException(401, 'Invalid credentials');
    }
    
    // Check if password is correct
    const isPasswordValid = await bcrypt.compare(password, user.password);
    
    if (!isPasswordValid) {
      throw new HttpException(401, 'Invalid credentials');
    }
    
    // Generate JWT
    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );
    
    // Return user data and token
    res.status(200).json({
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
        createdAt: user.createdAt.toISOString(),
        updatedAt: user.updatedAt.toISOString(),
      },
      token,
    });
  } catch (error) {
    next(error);
  }
};

// Get current user
export const getCurrentUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // User is set in auth middleware
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    const user = await prisma.user.findUnique({
      where: { id: userId },
    });
    
    if (!user) {
      throw new HttpException(404, 'User not found');
    }
    
    res.status(200).json({
      id: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
      role: user.role,
      createdAt: user.createdAt.toISOString(),
      updatedAt: user.updatedAt.toISOString(),
    });
  } catch (error) {
    next(error);
  }
}; 