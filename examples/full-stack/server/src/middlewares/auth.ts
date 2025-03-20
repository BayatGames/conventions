import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { HttpException } from './errorHandler';
import { prisma } from '../index';

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
      };
    }
  }
}

export const authenticateJWT = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // Get authorization header
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      throw new HttpException(401, 'No token provided');
    }
    
    // Check if format is correct (Bearer <token>)
    const parts = authHeader.split(' ');
    
    if (parts.length !== 2 || parts[0] !== 'Bearer') {
      throw new HttpException(401, 'Token format invalid');
    }
    
    const token = parts[1];
    
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret') as { userId: string };
    
    if (!decoded.userId) {
      throw new HttpException(401, 'Invalid token');
    }
    
    // Check if user exists
    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
    });
    
    if (!user) {
      throw new HttpException(401, 'User not found');
    }
    
    // Set user in request object
    req.user = { id: user.id };
    
    next();
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      next(new HttpException(401, 'Invalid token'));
    } else {
      next(error);
    }
  }
}; 