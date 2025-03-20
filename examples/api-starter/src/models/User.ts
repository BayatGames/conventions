import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { config } from '../config';

// User interface
export interface IUser {
  id: string;
  name: string;
  email: string;
  password: string;
  role: 'user' | 'admin';
  createdAt: Date;
  updatedAt: Date;
}

// User model class
export class User {
  // User data
  private data: Partial<IUser>;

  constructor(userData: Partial<IUser>) {
    this.data = userData;
  }

  // Get user data (without password)
  public toJSON(): Partial<IUser> {
    const { password, ...userWithoutPassword } = this.data;
    return userWithoutPassword;
  }

  // Hash password
  public async hashPassword(): Promise<void> {
    if (!this.data.password) {
      throw new Error('Password is required');
    }

    const salt = await bcrypt.genSalt(10);
    this.data.password = await bcrypt.hash(this.data.password, salt);
  }

  // Compare password
  public async comparePassword(candidatePassword: string): Promise<boolean> {
    if (!this.data.password) {
      throw new Error('User has no password');
    }

    return await bcrypt.compare(candidatePassword, this.data.password);
  }

  // Generate JWT token
  public generateAuthToken(): string {
    const payload = {
      id: this.data.id,
      email: this.data.email,
      role: this.data.role
    };

    return jwt.sign(payload, config.jwt.secret, {
      expiresIn: config.jwt.expiresIn
    });
  }

  // Generate refresh token
  public generateRefreshToken(): string {
    const payload = {
      id: this.data.id
    };

    return jwt.sign(payload, config.jwt.refreshSecret, {
      expiresIn: config.jwt.refreshExpiresIn
    });
  }
} 