import request from 'supertest';
import app from '../../src/app';
import jwt from 'jsonwebtoken';
import { config } from '../../src/config';

describe('User API', () => {
  // Mock authentication token
  let token: string;

  beforeAll(() => {
    // Create a test token for authentication
    token = jwt.sign(
      { id: 'test-user-id', email: 'test@example.com', role: 'admin' },
      config.jwt.secret,
      { expiresIn: '1h' }
    );
  });

  describe('GET /api/v1/users', () => {
    it('should return a list of users when authenticated', async () => {
      const response = await request(app)
        .get(`/api/${config.apiVersion}/users`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('success');
      expect(Array.isArray(response.body.data.users)).toBe(true);
    });

    it('should return 401 if not authenticated', async () => {
      const response = await request(app).get(`/api/${config.apiVersion}/users`);

      expect(response.status).toBe(401);
      expect(response.body.status).toBe('error');
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('should return a user when authenticated', async () => {
      const userId = '1';
      const response = await request(app)
        .get(`/api/${config.apiVersion}/users/${userId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('success');
      expect(response.body.data.user).toBeDefined();
      expect(response.body.data.user.id).toBe(userId);
    });

    it('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .get(`/api/${config.apiVersion}/users/999`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(404);
      expect(response.body.status).toBe('error');
    });
  });
}); 