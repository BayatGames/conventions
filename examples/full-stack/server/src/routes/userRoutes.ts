import { Router } from 'express';
import { getAllUsers, getUserById } from '../controllers/userController';
import { authenticateJWT } from '../middlewares/auth';

const router = Router();

// All routes require authentication
router.use(authenticateJWT);

// GET /api/users
router.get('/', getAllUsers);

// GET /api/users/:id
router.get('/:id', getUserById);

export default router; 