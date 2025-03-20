import mongoose, { Document, Schema } from 'mongoose';

// Notification types
export enum NotificationType {
  EMAIL = 'email',
  SMS = 'sms',
  PUSH = 'push'
}

// Notification status
export enum NotificationStatus {
  PENDING = 'pending',
  SENT = 'sent',
  FAILED = 'failed'
}

// Notification interface
export interface INotification extends Document {
  userId: string;
  type: NotificationType;
  title: string;
  content: string;
  status: NotificationStatus;
  recipient: string; // email address or phone number
  metadata: Record<string, any>;
  sentAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

// Notification schema
const NotificationSchema = new Schema<INotification>({
  userId: {
    type: String,
    required: true,
    index: true
  },
  type: {
    type: String,
    enum: Object.values(NotificationType),
    required: true
  },
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  status: {
    type: String,
    enum: Object.values(NotificationStatus),
    default: NotificationStatus.PENDING
  },
  recipient: {
    type: String,
    required: true
  },
  metadata: {
    type: Schema.Types.Mixed,
    default: {}
  },
  sentAt: {
    type: Date
  }
}, {
  timestamps: true
});

// Add index for querying by status
NotificationSchema.index({ status: 1 });

// Add index for filtering by created date
NotificationSchema.index({ createdAt: 1 });

// Create and export the Notification model
const Notification = mongoose.model<INotification>('Notification', NotificationSchema);
export default Notification; 