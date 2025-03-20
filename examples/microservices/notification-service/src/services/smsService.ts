import twilio from 'twilio';
import { NotificationStatus } from '../models/Notification';

// Initialize Twilio client
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

/**
 * Send SMS notification
 * 
 * @param to - Recipient phone number
 * @param content - SMS content
 * @param metadata - Additional metadata
 * @returns Promise with status and metadata
 */
export const sendSMS = async (
  to: string,
  content: string,
  metadata: Record<string, any> = {}
): Promise<{ status: NotificationStatus; metadata: Record<string, any> }> => {
  try {
    // Format phone number if needed
    const formattedPhoneNumber = formatPhoneNumber(to);
    
    // Send message
    const message = await client.messages.create({
      body: content,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: formattedPhoneNumber,
      ...metadata
    });
    
    return {
      status: NotificationStatus.SENT,
      metadata: {
        messageId: message.sid,
        status: message.status,
        errorCode: message.errorCode,
        errorMessage: message.errorMessage,
        timestamp: new Date().toISOString(),
      }
    };
  } catch (error) {
    console.error('Error sending SMS:', error);
    return {
      status: NotificationStatus.FAILED,
      metadata: {
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }
    };
  }
};

/**
 * Format phone number to E.164 format for Twilio
 * 
 * @param phoneNumber - Phone number to format
 * @returns Formatted phone number
 */
function formatPhoneNumber(phoneNumber: string): string {
  // Remove any non-digit characters
  const digitsOnly = phoneNumber.replace(/\D/g, '');
  
  // Check if the number already has a plus sign
  if (phoneNumber.startsWith('+')) {
    return phoneNumber;
  }
  
  // If number has 10 digits, assume US number
  if (digitsOnly.length === 10) {
    return `+1${digitsOnly}`;
  }
  
  // Otherwise, add + prefix
  return `+${digitsOnly}`;
} 