import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { 
  login, 
  logout, 
  getCurrentUser, 
  setCredentials, 
  clearCredentials 
} from '../store/slices/authSlice';

/**
 * Custom hook for authentication
 * Provides authentication state and methods
 */
export const useAuth = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  
  // Auth state from Redux store
  const { user, token, isAuthenticated, isLoading, error } = useAppSelector(
    (state) => state.auth
  );

  /**
   * Login with email and password
   */
  const loginUser = useCallback(
    async (email: string, password: string) => {
      try {
        await dispatch(login({ email, password })).unwrap();
        navigate('/dashboard');
        return true;
      } catch (error) {
        return false;
      }
    },
    [dispatch, navigate]
  );

  /**
   * Logout current user
   */
  const logoutUser = useCallback(async () => {
    await dispatch(logout());
    navigate('/login');
  }, [dispatch, navigate]);

  /**
   * Get current user info
   */
  const fetchCurrentUser = useCallback(async () => {
    if (token) {
      await dispatch(getCurrentUser());
    }
  }, [dispatch, token]);

  /**
   * Set authentication credentials
   */
  const setAuth = useCallback(
    (userData: { user: any; token: string }) => {
      dispatch(setCredentials(userData));
    },
    [dispatch]
  );

  /**
   * Clear authentication data
   */
  const clearAuth = useCallback(() => {
    dispatch(clearCredentials());
  }, [dispatch]);

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    loginUser,
    logoutUser,
    fetchCurrentUser,
    setAuth,
    clearAuth,
  };
}; 