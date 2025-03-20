import nodemailer from 'nodemailer';
import { NotificationStatus } from '../models/Notification';

// Email configuration
const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST,
  port: parseInt(process.env.EMAIL_PORT || '587'),
  secure: process.env.EMAIL_PORT === '465',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASSWORD,
  },
});

/**
 * Send email notification
 * 
 * @param to - Recipient email address
 * @param subject - Email subject
 * @param content - Email content (HTML)
 * @param metadata - Additional metadata
 * @returns Promise with status and metadata
 */
export const sendEmail = async (
  to: string,
  subject: string,
  content: string,
  metadata: Record<string, any> = {}
): Promise<{ status: NotificationStatus; metadata: Record<string, any> }> => {
  try {
    const mailOptions = {
      from: process.env.EMAIL_FROM || 'no-reply@example.com',
      to,
      subject,
      html: content,
      ...metadata
    };

    const info = await transporter.sendMail(mailOptions);
    
    return {
      status: NotificationStatus.SENT,
      metadata: {
        messageId: info.messageId,
        response: info.response,
        envelope: info.envelope,
        timestamp: new Date().toISOString(),
      }
    };
  } catch (error) {
    console.error('Error sending email:', error);
    return {
      status: NotificationStatus.FAILED,
      metadata: {
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }
    };
  }
}; 