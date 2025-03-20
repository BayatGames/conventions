import express from 'express';
import userRoutes from './userRoutes';

const router = express.Router();

// Root route
router.get('/', (req, res) => {
  res.status(200).json({
    status: 'success',
    message: 'Welcome to the Bayat API',
  });
});

// Register all route modules
router.use('/users', userRoutes);

export default router; 