import { Router } from 'express';
import { body } from 'express-validator';
import * as productController from '../controllers/productController';
import { authenticate, isAdmin } from '../middleware/auth';
import { upload } from '../utils/upload';

const router = Router();

// GET /products - Get all products with pagination and filtering
router.get('/', productController.getProducts);

// GET /products/:id - Get product by ID
router.get('/:id', productController.getProductById);

// POST /products - Create a new product (admin only)
router.post(
  '/', 
  authenticate,
  isAdmin,
  upload.single('image'),
  [
    body('name').trim().notEmpty().withMessage('Product name is required'),
    body('description').trim().notEmpty().withMessage('Description is required'),
    body('price').isFloat({ min: 0.01 }).withMessage('Price must be greater than 0'),
    body('category').notEmpty().withMessage('Category is required'),
    body('sku').notEmpty().withMessage('SKU is required'),
    body('inventory').isInt({ min: 0 }).withMessage('Inventory must be a positive number'),
    body('features').optional().isArray(),
    body('dimensions').optional().isObject(),
  ],
  productController.createProduct
);

// PUT /products/:id - Update a product (admin only)
router.put(
  '/:id', 
  authenticate,
  isAdmin,
  upload.single('image'),
  [
    body('name').optional().trim().notEmpty().withMessage('Product name cannot be empty'),
    body('description').optional().trim().notEmpty().withMessage('Description cannot be empty'),
    body('price').optional().isFloat({ min: 0.01 }).withMessage('Price must be greater than 0'),
    body('category').optional().notEmpty().withMessage('Category cannot be empty'),
    body('sku').optional().notEmpty().withMessage('SKU cannot be empty'),
    body('inventory').optional().isInt({ min: 0 }).withMessage('Inventory must be a positive number'),
    body('features').optional().isArray(),
    body('dimensions').optional().isObject(),
    body('isActive').optional().isBoolean(),
  ],
  productController.updateProduct
);

// DELETE /products/:id - Delete a product (admin only, soft delete)
router.delete('/:id', authenticate, isAdmin, productController.deleteProduct);

// PATCH /products/:id/inventory - Update product inventory (admin only)
router.patch(
  '/:id/inventory',
  authenticate,
  isAdmin,
  [
    body('inventory').isInt({ min: 0 }).withMessage('Inventory must be a positive number'),
  ],
  productController.updateInventory
);

export default router; 