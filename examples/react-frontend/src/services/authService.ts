import api from './api';
import { User } from '../store/slices/authSlice';

/**
 * Authentication service
 * Provides methods for user authentication and management
 */
const authService = {
  /**
   * Login user with email and password
   * @param email User email
   * @param password User password
   * @returns User data and token
   */
  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  /**
   * Register a new user
   * @param username Username
   * @param email User email
   * @param password User password
   * @returns User data and token
   */
  async register(username: string, email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data;
  },

  /**
   * Logout the current user
   */
  async logout(): Promise<void> {
    await api.post('/auth/logout');
  },

  /**
   * Get the currently authenticated user
   * @returns User data
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data.user;
  },

  /**
   * Update user profile
   * @param userData User data to update
   * @returns Updated user data
   */
  async updateProfile(userData: Partial<User>): Promise<User> {
    const response = await api.put('/auth/profile', userData);
    return response.data.user;
  },

  /**
   * Change user password
   * @param currentPassword Current password
   * @param newPassword New password
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await api.put('/auth/password', { currentPassword, newPassword });
  },

  /**
   * Request password reset
   * @param email User email
   */
  async forgotPassword(email: string): Promise<void> {
    await api.post('/auth/forgot-password', { email });
  },

  /**
   * Reset password with token
   * @param token Reset token
   * @param newPassword New password
   */
  async resetPassword(token: string, newPassword: string): Promise<void> {
    await api.post('/auth/reset-password', { token, newPassword });
  }
};

export default authService; 