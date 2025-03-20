import { Router } from 'express';
import { body } from 'express-validator';
import { 
  getAllTodos, 
  getTodoById, 
  createTodo, 
  updateTodo, 
  deleteTodo 
} from '../controllers/todoController';
import { authenticateJWT } from '../middlewares/auth';

const router = Router();

// All routes require authentication
router.use(authenticateJWT);

// GET /api/todos
router.get('/', getAllTodos);

// GET /api/todos/:id
router.get('/:id', getTodoById);

// POST /api/todos
router.post(
  '/',
  [
    body('title').not().isEmpty().withMessage('Title is required'),
    body('description').optional(),
  ],
  createTodo
);

// PUT /api/todos/:id
router.put(
  '/:id',
  [
    body('title').optional(),
    body('description').optional(),
    body('completed').optional().isBoolean().withMessage('Completed must be a boolean'),
  ],
  updateTodo
);

// DELETE /api/todos/:id
router.delete('/:id', deleteTodo);

export default router; 