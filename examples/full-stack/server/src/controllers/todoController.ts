import { Request, Response, NextFunction } from 'express';
import { validationResult } from 'express-validator';
import { prisma } from '../index';
import { HttpException } from '../middlewares/errorHandler';
import { CreateTodoRequest, UpdateTodoRequest } from 'shared/types';

// Get all todos for the current user
export const getAllTodos = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    const todos = await prisma.todo.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
    });
    
    return res.status(200).json(todos.map(todo => ({
      ...todo,
      createdAt: todo.createdAt.toISOString(),
      updatedAt: todo.updatedAt.toISOString(),
    })));
  } catch (error) {
    next(error);
  }
};

// Get a todo by ID
export const getTodoById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    const todo = await prisma.todo.findUnique({
      where: { id },
    });
    
    if (!todo) {
      throw new HttpException(404, 'Todo not found');
    }
    
    // Check if the todo belongs to the user
    if (todo.userId !== userId) {
      throw new HttpException(403, 'Forbidden');
    }
    
    return res.status(200).json({
      ...todo,
      createdAt: todo.createdAt.toISOString(),
      updatedAt: todo.updatedAt.toISOString(),
    });
  } catch (error) {
    next(error);
  }
};

// Create a new todo
export const createTodo = async (req: Request, res: Response, next: NextFunction) => {
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
    
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    const { title, description } = req.body as CreateTodoRequest;
    
    const newTodo = await prisma.todo.create({
      data: {
        title,
        description,
        userId,
      },
    });
    
    return res.status(201).json({
      ...newTodo,
      createdAt: newTodo.createdAt.toISOString(),
      updatedAt: newTodo.updatedAt.toISOString(),
    });
  } catch (error) {
    next(error);
  }
};

// Update a todo
export const updateTodo = async (req: Request, res: Response, next: NextFunction) => {
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
    
    const { id } = req.params;
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    // Check if todo exists and belongs to user
    const existingTodo = await prisma.todo.findUnique({
      where: { id },
    });
    
    if (!existingTodo) {
      throw new HttpException(404, 'Todo not found');
    }
    
    if (existingTodo.userId !== userId) {
      throw new HttpException(403, 'Forbidden');
    }
    
    const { title, description, completed } = req.body as UpdateTodoRequest;
    
    const updatedTodo = await prisma.todo.update({
      where: { id },
      data: {
        ...(title !== undefined && { title }),
        ...(description !== undefined && { description }),
        ...(completed !== undefined && { completed }),
      },
    });
    
    return res.status(200).json({
      ...updatedTodo,
      createdAt: updatedTodo.createdAt.toISOString(),
      updatedAt: updatedTodo.updatedAt.toISOString(),
    });
  } catch (error) {
    next(error);
  }
};

// Delete a todo
export const deleteTodo = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const userId = req.user?.id;
    
    if (!userId) {
      throw new HttpException(401, 'Unauthorized');
    }
    
    // Check if todo exists and belongs to user
    const existingTodo = await prisma.todo.findUnique({
      where: { id },
    });
    
    if (!existingTodo) {
      throw new HttpException(404, 'Todo not found');
    }
    
    if (existingTodo.userId !== userId) {
      throw new HttpException(403, 'Forbidden');
    }
    
    await prisma.todo.delete({
      where: { id },
    });
    
    return res.status(204).send();
  } catch (error) {
    next(error);
  }
}; 