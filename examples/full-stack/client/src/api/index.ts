import axios from 'axios';
import { LoginCredentials, RegisterCredentials, User } from 'shared';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:4000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
const authApi = {
  login: async (credentials: LoginCredentials) => {
    const response = await apiClient.post<{ user: User; token: string }>('/auth/login', credentials);
    return response.data;
  },
  register: async (credentials: RegisterCredentials) => {
    const response = await apiClient.post<{ user: User; token: string }>('/auth/register', credentials);
    return response.data;
  },
  getCurrentUser: async () => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};

// Users API
const usersApi = {
  getAll: async () => {
    const response = await apiClient.get<User[]>('/users');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<User>(`/users/${id}`);
    return response.data;
  },
};

export const api = {
  auth: authApi,
  users: usersApi,
}; 