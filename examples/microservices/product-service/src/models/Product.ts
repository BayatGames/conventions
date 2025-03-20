import mongoose, { Document, Schema } from 'mongoose';

// Product category enum
export enum ProductCategory {
  ELECTRONICS = 'electronics',
  CLOTHING = 'clothing',
  BOOKS = 'books',
  HOME = 'home',
  BEAUTY = 'beauty',
  SPORTS = 'sports',
  TOYS = 'toys',
  FOOD = 'food',
  OTHER = 'other'
}

// Product interface
export interface IProduct extends Document {
  name: string;
  description: string;
  price: number;
  category: ProductCategory;
  imageUrl?: string;
  sku: string;
  inventory: number;
  features?: string[];
  dimensions?: {
    width?: number;
    height?: number;
    depth?: number;
    weight?: number;
  };
  ratings?: {
    average: number;
    count: number;
  };
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Product schema
const ProductSchema = new Schema<IProduct>(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      index: true
    },
    description: {
      type: String,
      required: true
    },
    price: {
      type: Number,
      required: true,
      min: 0
    },
    category: {
      type: String,
      enum: Object.values(ProductCategory),
      required: true,
      index: true
    },
    imageUrl: {
      type: String
    },
    sku: {
      type: String,
      required: true,
      unique: true,
      index: true
    },
    inventory: {
      type: Number,
      required: true,
      min: 0,
      default: 0
    },
    features: {
      type: [String]
    },
    dimensions: {
      width: Number,
      height: Number,
      depth: Number,
      weight: Number
    },
    ratings: {
      average: {
        type: Number,
        min: 0,
        max: 5,
        default: 0
      },
      count: {
        type: Number,
        default: 0
      }
    },
    isActive: {
      type: Boolean,
      default: true,
      index: true
    }
  },
  {
    timestamps: true
  }
);

// Create and export the Product model
const Product = mongoose.model<IProduct>('Product', ProductSchema);
export default Product; 