import { Kafka, Consumer } from 'kafkajs';
import Notification, { NotificationType } from '../models/Notification';
import { sendEmail } from '../services/emailService';
import { sendSMS } from '../services/smsService';

// Event types that this service will consume
enum EventType {
  USER_CREATED = 'USER_CREATED',
  USER_UPDATED = 'USER_UPDATED',
  USER_DELETED = 'USER_DELETED',
  ORDER_CREATED = 'ORDER_CREATED',
  ORDER_UPDATED = 'ORDER_UPDATED',
  ORDER_SHIPPED = 'ORDER_SHIPPED',
  ORDER_DELIVERED = 'ORDER_DELIVERED',
  ORDER_CANCELLED = 'ORDER_CANCELLED'
}

// Initialize Kafka
const kafka = new Kafka({
  clientId: process.env.KAFKA_CLIENT_ID || 'notification-service',
  brokers: (process.env.KAFKA_BROKERS || 'localhost:9092').split(','),
});

// Create consumer
const consumer = kafka.consumer({
  groupId: process.env.KAFKA_GROUP_ID || 'notification-service-group',
});

/**
 * Start the Kafka consumer
 */
export const startConsumer = async (): Promise<void> => {
  try {
    // Connect to Kafka
    await consumer.connect();
    console.log('Connected to Kafka');
    
    // Subscribe to topics
    await consumer.subscribe({
      topics: [
        'user-events',
        'order-events'
      ],
      fromBeginning: false,
    });
    
    // Start consuming messages
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        if (!message.value) return;
        
        try {
          const eventData = JSON.parse(message.value.toString());
          console.log(`Received event: ${eventData.type} from topic: ${topic}`);
          
          // Process event based on type
          await processEvent(eventData);
        } catch (error) {
          console.error('Error processing message:', error);
        }
      },
    });
  } catch (error) {
    console.error('Failed to start Kafka consumer:', error);
    throw error;
  }
};

/**
 * Process received event and send appropriate notifications
 * 
 * @param eventData - Event data from Kafka
 */
const processEvent = async (eventData: any): Promise<void> => {
  try {
    // Extract common data
    const { type, payload, timestamp } = eventData;
    
    switch (type) {
      case EventType.USER_CREATED:
        await handleUserCreated(payload);
        break;
      
      case EventType.ORDER_CREATED:
        await handleOrderCreated(payload);
        break;
      
      case EventType.ORDER_UPDATED:
        await handleOrderUpdated(payload);
        break;
      
      case EventType.ORDER_SHIPPED:
        await handleOrderShipped(payload);
        break;
      
      case EventType.ORDER_DELIVERED:
        await handleOrderDelivered(payload);
        break;
      
      case EventType.ORDER_CANCELLED:
        await handleOrderCancelled(payload);
        break;
      
      default:
        console.log(`Event type ${type} not handled`);
    }
  } catch (error) {
    console.error('Error processing event:', error);
  }
};

/**
 * Handle USER_CREATED event
 */
const handleUserCreated = async (payload: any): Promise<void> => {
  const { user } = payload;
  
  // Create welcome email notification
  const notification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Welcome to our platform!',
    content: `
      <h1>Welcome ${user.firstName}!</h1>
      <p>Thank you for joining our platform. We're excited to have you!</p>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { userCreatedAt: user.createdAt }
  });
  
  // Save notification to database
  await notification.save();
  
  // Send email
  const result = await sendEmail(
    user.email,
    'Welcome to our platform!',
    notification.content,
    { userId: user._id }
  );
  
  // Update notification status
  notification.status = result.status;
  notification.metadata = { ...notification.metadata, ...result.metadata };
  notification.sentAt = new Date();
  await notification.save();
};

/**
 * Handle ORDER_CREATED event
 */
const handleOrderCreated = async (payload: any): Promise<void> => {
  const { order, user } = payload;
  
  // Create order confirmation email
  const emailNotification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Order Confirmation',
    content: `
      <h1>Order Confirmation</h1>
      <p>Dear ${user.firstName},</p>
      <p>Thank you for your order #${order._id}!</p>
      <p>We've received your order and are processing it.</p>
      <p>Order Total: $${order.totalAmount.toFixed(2)}</p>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { orderId: order._id }
  });
  
  // Create order confirmation SMS
  const smsNotification = new Notification({
    userId: user._id,
    type: NotificationType.SMS,
    title: 'Order Confirmation',
    content: `Your order #${order._id} for $${order.totalAmount.toFixed(2)} has been received and is being processed.`,
    recipient: user.phone,
    metadata: { orderId: order._id }
  });
  
  // Save notifications
  await emailNotification.save();
  await smsNotification.save();
  
  // Send notifications
  const emailResult = await sendEmail(
    user.email,
    'Order Confirmation',
    emailNotification.content,
    { orderId: order._id }
  );
  
  const smsResult = await sendSMS(
    user.phone,
    smsNotification.content,
    { orderId: order._id }
  );
  
  // Update email notification status
  emailNotification.status = emailResult.status;
  emailNotification.metadata = { ...emailNotification.metadata, ...emailResult.metadata };
  emailNotification.sentAt = new Date();
  await emailNotification.save();
  
  // Update SMS notification status
  smsNotification.status = smsResult.status;
  smsNotification.metadata = { ...smsNotification.metadata, ...smsResult.metadata };
  smsNotification.sentAt = new Date();
  await smsNotification.save();
};

/**
 * Handle ORDER_UPDATED event
 */
const handleOrderUpdated = async (payload: any): Promise<void> => {
  const { order, user, changes } = payload;
  
  // Create order update email
  const notification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Order Update',
    content: `
      <h1>Order Update</h1>
      <p>Dear ${user.firstName},</p>
      <p>Your order #${order._id} has been updated.</p>
      <p>The following changes have been made:</p>
      <ul>
        ${Object.entries(changes).map(([key, value]) => `<li>${key}: ${value}</li>`).join('')}
      </ul>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { orderId: order._id, changes }
  });
  
  // Save notification
  await notification.save();
  
  // Send email
  const result = await sendEmail(
    user.email,
    'Order Update',
    notification.content,
    { orderId: order._id }
  );
  
  // Update notification status
  notification.status = result.status;
  notification.metadata = { ...notification.metadata, ...result.metadata };
  notification.sentAt = new Date();
  await notification.save();
};

/**
 * Handle ORDER_SHIPPED event
 */
const handleOrderShipped = async (payload: any): Promise<void> => {
  const { order, user, tracking } = payload;
  
  // Create order shipped email
  const emailNotification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Your Order Has Shipped',
    content: `
      <h1>Your Order Has Shipped</h1>
      <p>Dear ${user.firstName},</p>
      <p>Great news! Your order #${order._id} has been shipped.</p>
      <p>Tracking number: ${tracking.trackingNumber}</p>
      <p>Carrier: ${tracking.carrier}</p>
      <p>Estimated delivery: ${tracking.estimatedDelivery}</p>
      <p>Track your order: <a href="${tracking.trackingUrl}">Click here</a></p>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { orderId: order._id, tracking }
  });
  
  // Create order shipped SMS
  const smsNotification = new Notification({
    userId: user._id,
    type: NotificationType.SMS,
    title: 'Order Shipped',
    content: `Your order #${order._id} has shipped! Track: ${tracking.trackingUrl} (${tracking.carrier}: ${tracking.trackingNumber})`,
    recipient: user.phone,
    metadata: { orderId: order._id, tracking }
  });
  
  // Save notifications
  await emailNotification.save();
  await smsNotification.save();
  
  // Send notifications
  const emailResult = await sendEmail(
    user.email,
    'Your Order Has Shipped',
    emailNotification.content,
    { orderId: order._id }
  );
  
  const smsResult = await sendSMS(
    user.phone,
    smsNotification.content,
    { orderId: order._id }
  );
  
  // Update email notification status
  emailNotification.status = emailResult.status;
  emailNotification.metadata = { ...emailNotification.metadata, ...emailResult.metadata };
  emailNotification.sentAt = new Date();
  await emailNotification.save();
  
  // Update SMS notification status
  smsNotification.status = smsResult.status;
  smsNotification.metadata = { ...smsNotification.metadata, ...smsResult.metadata };
  smsNotification.sentAt = new Date();
  await smsNotification.save();
};

/**
 * Handle ORDER_DELIVERED event
 */
const handleOrderDelivered = async (payload: any): Promise<void> => {
  const { order, user } = payload;
  
  // Create order delivered email
  const notification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Your Order Has Been Delivered',
    content: `
      <h1>Your Order Has Been Delivered</h1>
      <p>Dear ${user.firstName},</p>
      <p>Your order #${order._id} has been delivered.</p>
      <p>We hope you enjoy your purchase! If you have any questions or concerns, please contact our customer service.</p>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { orderId: order._id }
  });
  
  // Save notification
  await notification.save();
  
  // Send email
  const result = await sendEmail(
    user.email,
    'Your Order Has Been Delivered',
    notification.content,
    { orderId: order._id }
  );
  
  // Update notification status
  notification.status = result.status;
  notification.metadata = { ...notification.metadata, ...result.metadata };
  notification.sentAt = new Date();
  await notification.save();
};

/**
 * Handle ORDER_CANCELLED event
 */
const handleOrderCancelled = async (payload: any): Promise<void> => {
  const { order, user, reason } = payload;
  
  // Create order cancelled email
  const notification = new Notification({
    userId: user._id,
    type: NotificationType.EMAIL,
    title: 'Order Cancellation',
    content: `
      <h1>Order Cancellation</h1>
      <p>Dear ${user.firstName},</p>
      <p>Your order #${order._id} has been cancelled.</p>
      <p>Reason: ${reason || 'Not specified'}</p>
      <p>If you have any questions or concerns, please contact our customer service.</p>
      <p>Best regards,<br>The Team</p>
    `,
    recipient: user.email,
    metadata: { orderId: order._id, reason }
  });
  
  // Save notification
  await notification.save();
  
  // Send email
  const result = await sendEmail(
    user.email,
    'Order Cancellation',
    notification.content,
    { orderId: order._id }
  );
  
  // Update notification status
  notification.status = result.status;
  notification.metadata = { ...notification.metadata, ...result.metadata };
  notification.sentAt = new Date();
  await notification.save();
}; 