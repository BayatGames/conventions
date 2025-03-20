import express, { Router } from 'express';
import { authenticate } from '../middleware/auth';

const router: Router = express.Router();

/**
 * @swagger
 * /api/v1/users:
 *   get:
 *     summary: Get all users
 *     description: Retrieve a list of all users. Requires authentication.
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: A list of users
 */
router.get('/', authenticate, (req, res) => {
  // This is a placeholder. In a real implementation, this would call a controller method
  res.status(200).json({
    status: 'success',
    message: 'List of users',
    data: {
      users: [],
    },
  });
});

/**
 * @swagger
 * /api/v1/users/{id}:
 *   get:
 *     summary: Get a user by ID
 *     description: Retrieve a single user by their ID. Requires authentication.
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: User ID
 *     responses:
 *       200:
 *         description: User details
 *       404:
 *         description: User not found
 */
router.get('/:id', authenticate, (req, res) => {
  // This is a placeholder. In a real implementation, this would call a controller method
  res.status(200).json({
    status: 'success',
    message: `User with ID ${req.params.id}`,
    data: {
      user: {
        id: req.params.id,
        name: 'Example User',
        email: 'user@example.com',
      },
    },
  });
});

export default router; 