import { Request, Response } from 'express';
import { validationResult } from 'express-validator';
import { Kafka } from 'kafkajs';
import Product, { ProductCategory } from '../models/Product';

// Get all products with pagination and filtering
export const getProducts = async (req: Request, res: Response) => {
  try {
    // Extract query parameters
    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 20;
    const sortBy = req.query.sortBy as string || 'createdAt';
    const sortOrder = req.query.sortOrder as string === 'asc' ? 1 : -1;
    const category = req.query.category as string;
    const search = req.query.search as string;
    const minPrice = parseFloat(req.query.minPrice as string) || 0;
    const maxPrice = parseFloat(req.query.maxPrice as string) || Number.MAX_SAFE_INTEGER;
    const inStock = req.query.inStock === 'true';

    // Build filter
    const filter: any = { isActive: true };

    // Category filter
    if (category && Object.values(ProductCategory).includes(category as ProductCategory)) {
      filter.category = category;
    }

    // Price range filter
    filter.price = { $gte: minPrice, $lte: maxPrice };

    // In stock filter
    if (inStock) {
      filter.inventory = { $gt: 0 };
    }

    // Search filter
    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } },
        { sku: { $regex: search, $options: 'i' } }
      ];
    }

    // Calculate pagination
    const skip = (page - 1) * limit;

    // Build sort
    const sort: any = {};
    sort[sortBy] = sortOrder;

    // Execute query with pagination
    const products = await Product.find(filter)
      .sort(sort)
      .skip(skip)
      .limit(limit);

    // Get total count for pagination
    const total = await Product.countDocuments(filter);

    // Send response
    res.json({
      products,
      pagination: {
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('Error in getProducts controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Get product by ID
export const getProductById = async (req: Request, res: Response) => {
  try {
    const product = await Product.findById(req.params.id);
    
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    if (!product.isActive) {
      return res.status(404).json({ message: 'Product is not available' });
    }

    res.json(product);
  } catch (error) {
    console.error('Error in getProductById controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Create a new product
export const createProduct = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Check if user is admin
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const { 
      name, 
      description, 
      price, 
      category, 
      sku, 
      inventory, 
      features, 
      dimensions 
    } = req.body;

    // Check if product with SKU already exists
    const existingProduct = await Product.findOne({ sku });
    if (existingProduct) {
      return res.status(400).json({ message: 'Product with this SKU already exists' });
    }

    // Set image URL if file was uploaded
    let imageUrl;
    if (req.file) {
      // In a real app, you might store this in S3 or another service
      // and return a CDN URL
      imageUrl = `/uploads/${req.file.filename}`;
    }

    // Create new product
    const product = new Product({
      name,
      description,
      price,
      category,
      sku,
      inventory,
      features,
      dimensions,
      imageUrl
    });

    await product.save();

    // Emit product created event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'product-events',
      messages: [
        {
          key: product.id,
          value: JSON.stringify({
            type: 'PRODUCT_CREATED',
            payload: {
              product: {
                _id: product.id,
                name: product.name,
                price: product.price,
                category: product.category,
                sku: product.sku,
                inventory: product.inventory
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.status(201).json({
      message: 'Product created successfully',
      product
    });
  } catch (error) {
    console.error('Error in createProduct controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Update a product
export const updateProduct = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Check if user is admin
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const product = await Product.findById(req.params.id);
    
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    const { 
      name, 
      description, 
      price, 
      category, 
      inventory, 
      features, 
      dimensions,
      isActive
    } = req.body;

    // Check if SKU is being updated and if it already exists
    if (req.body.sku && req.body.sku !== product.sku) {
      const existingProduct = await Product.findOne({ sku: req.body.sku });
      if (existingProduct) {
        return res.status(400).json({ message: 'Product with this SKU already exists' });
      }
      product.sku = req.body.sku;
    }

    // Update fields if provided
    if (name) product.name = name;
    if (description) product.description = description;
    if (price !== undefined) product.price = price;
    if (category) product.category = category;
    if (inventory !== undefined) product.inventory = inventory;
    if (features) product.features = features;
    if (dimensions) product.dimensions = dimensions;
    if (isActive !== undefined) product.isActive = isActive;

    // Set image URL if file was uploaded
    if (req.file) {
      product.imageUrl = `/uploads/${req.file.filename}`;
    }

    await product.save();

    // Emit product updated event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'product-events',
      messages: [
        {
          key: product.id,
          value: JSON.stringify({
            type: 'PRODUCT_UPDATED',
            payload: {
              product: {
                _id: product.id,
                name: product.name,
                price: product.price,
                category: product.category,
                sku: product.sku,
                inventory: product.inventory,
                isActive: product.isActive
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Product updated successfully',
      product
    });
  } catch (error) {
    console.error('Error in updateProduct controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Delete a product (soft delete)
export const deleteProduct = async (req: Request, res: Response) => {
  try {
    // Check if user is admin
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const product = await Product.findById(req.params.id);
    
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    // Soft delete (set inactive)
    product.isActive = false;
    await product.save();

    // Emit product deleted event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'product-events',
      messages: [
        {
          key: product.id,
          value: JSON.stringify({
            type: 'PRODUCT_DELETED',
            payload: {
              product: {
                _id: product.id,
                name: product.name,
                sku: product.sku
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Product deleted successfully'
    });
  } catch (error) {
    console.error('Error in deleteProduct controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Update product inventory
export const updateInventory = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Check if user is admin
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const { inventory } = req.body;
    
    const product = await Product.findById(req.params.id);
    
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    // Update inventory
    product.inventory = inventory;
    await product.save();

    // Emit inventory updated event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'product-events',
      messages: [
        {
          key: product.id,
          value: JSON.stringify({
            type: 'PRODUCT_INVENTORY_UPDATED',
            payload: {
              product: {
                _id: product.id,
                name: product.name,
                sku: product.sku,
                inventory: product.inventory
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Product inventory updated successfully',
      product
    });
  } catch (error) {
    console.error('Error in updateInventory controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
}; 