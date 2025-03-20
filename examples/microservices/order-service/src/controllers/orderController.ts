import { Request, Response } from 'express';
import { validationResult } from 'express-validator';
import Order, { OrderStatus } from '../models/Order';
import { Kafka } from 'kafkajs';

// Create a new order
export const createOrder = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { items, shippingAddress, paymentMethod } = req.body;
    const userId = req.userId;

    // Create new order
    const order = new Order({
      userId,
      items,
      shippingAddress,
      paymentMethod,
      status: OrderStatus.PENDING,
      paymentStatus: 'pending'
    });

    await order.save();

    // Emit order created event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'order-events',
      messages: [
        {
          key: order.id,
          value: JSON.stringify({
            type: 'ORDER_CREATED',
            payload: {
              order: {
                _id: order.id,
                items: order.items,
                totalAmount: order.totalAmount,
                status: order.status
              },
              user: {
                _id: userId,
                // In a real app, you might fetch more user details here
                // or use a user service client to get them
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.status(201).json({
      message: 'Order created successfully',
      order
    });
  } catch (error) {
    console.error('Error in createOrder controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Get all orders for a user
export const getUserOrders = async (req: Request, res: Response) => {
  try {
    const userId = req.userId;
    const orders = await Order.find({ userId }).sort({ createdAt: -1 });

    res.json(orders);
  } catch (error) {
    console.error('Error in getUserOrders controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Get all orders (admin only)
export const getAllOrders = async (req: Request, res: Response) => {
  try {
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const orders = await Order.find().sort({ createdAt: -1 });
    res.json(orders);
  } catch (error) {
    console.error('Error in getAllOrders controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Get order by ID
export const getOrderById = async (req: Request, res: Response) => {
  try {
    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Check if the user has access to this order
    if (req.userRole !== 'admin' && order.userId !== req.userId) {
      return res.status(403).json({ message: 'Forbidden - You do not have access to this order' });
    }

    res.json(order);
  } catch (error) {
    console.error('Error in getOrderById controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Update order status
export const updateOrderStatus = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { status } = req.body;
    
    // Only admins can update order status
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Update status
    const oldStatus = order.status;
    order.status = status;
    await order.save();

    // Determine event type based on status
    let eventType: string;
    switch (status) {
      case OrderStatus.SHIPPED:
        eventType = 'ORDER_SHIPPED';
        break;
      case OrderStatus.DELIVERED:
        eventType = 'ORDER_DELIVERED';
        break;
      case OrderStatus.CANCELLED:
        eventType = 'ORDER_CANCELLED';
        break;
      default:
        eventType = 'ORDER_UPDATED';
    }

    // Emit event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'order-events',
      messages: [
        {
          key: order.id,
          value: JSON.stringify({
            type: eventType,
            payload: {
              order: {
                _id: order.id,
                items: order.items,
                totalAmount: order.totalAmount,
                status: order.status
              },
              user: {
                _id: order.userId,
                // In a real app, you would fetch more user details
              },
              changes: {
                status: {
                  from: oldStatus,
                  to: status
                }
              },
              // If shipping event, include tracking info
              ...(status === OrderStatus.SHIPPED && {
                tracking: {
                  trackingNumber: req.body.trackingNumber || 'TRACK123456789',
                  carrier: req.body.carrier || 'Default Carrier',
                  estimatedDelivery: req.body.estimatedDelivery || new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(),
                  trackingUrl: req.body.trackingUrl || 'https://example.com/track'
                }
              })
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Order status updated successfully',
      order
    });
  } catch (error) {
    console.error('Error in updateOrderStatus controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Update payment status
export const updatePaymentStatus = async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { paymentStatus } = req.body;
    
    // Only admins can update payment status
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Forbidden - Admin access required' });
    }

    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Update payment status
    const oldPaymentStatus = order.paymentStatus;
    order.paymentStatus = paymentStatus;
    await order.save();

    // Emit order updated event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'order-events',
      messages: [
        {
          key: order.id,
          value: JSON.stringify({
            type: 'ORDER_UPDATED',
            payload: {
              order: {
                _id: order.id,
                totalAmount: order.totalAmount,
                status: order.status,
                paymentStatus: order.paymentStatus
              },
              user: {
                _id: order.userId,
                // In a real app, you would fetch more user details
              },
              changes: {
                paymentStatus: {
                  from: oldPaymentStatus,
                  to: paymentStatus
                }
              }
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Payment status updated successfully',
      order
    });
  } catch (error) {
    console.error('Error in updatePaymentStatus controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// Cancel order
export const cancelOrder = async (req: Request, res: Response) => {
  try {
    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Check if the user has access to this order
    if (req.userRole !== 'admin' && order.userId !== req.userId) {
      return res.status(403).json({ message: 'Forbidden - You do not have access to this order' });
    }

    // Check if order can be cancelled
    if (order.status === OrderStatus.SHIPPED || order.status === OrderStatus.DELIVERED) {
      return res.status(400).json({ 
        message: `Order cannot be cancelled because it is already ${order.status}` 
      });
    }

    // Update status
    const oldStatus = order.status;
    order.status = OrderStatus.CANCELLED;
    await order.save();

    // Emit order cancelled event
    const producer = req.app.locals.kafkaProducer as Kafka['producer'];
    await producer.send({
      topic: 'order-events',
      messages: [
        {
          key: order.id,
          value: JSON.stringify({
            type: 'ORDER_CANCELLED',
            payload: {
              order: {
                _id: order.id,
                items: order.items,
                totalAmount: order.totalAmount,
                status: order.status
              },
              user: {
                _id: order.userId,
                // In a real app, you would fetch more user details
              },
              changes: {
                status: {
                  from: oldStatus,
                  to: OrderStatus.CANCELLED
                }
              },
              reason: req.body.reason || 'Cancelled by user'
            },
            timestamp: new Date().toISOString(),
          }),
        },
      ],
    });

    res.json({
      message: 'Order cancelled successfully',
      order
    });
  } catch (error) {
    console.error('Error in cancelOrder controller:', error);
    res.status(500).json({ message: 'Server error' });
  }
}; 