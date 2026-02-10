/**
 * JWT Token Storage Utility
 *
 * Handles secure storage and retrieval of JWT tokens from browser localStorage.
 * Provides functions to save, retrieve, and clear JWT tokens.
 */

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

export interface StoredUser {
  id: string;
  email: string;
  name?: string;
}

/**
 * Save JWT token and user data to localStorage
 */
export function saveToken(token: string, user?: StoredUser): void {
  try {
    localStorage.setItem(TOKEN_KEY, token);
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    }
  } catch (error) {
    console.error('Failed to save token:', error);
  }
}

/**
 * Retrieve JWT token from localStorage
 */
export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error('Failed to retrieve token:', error);
    return null;
  }
}

/**
 * Retrieve stored user data from localStorage
 */
export function getUser(): StoredUser | null {
  try {
    const userJson = localStorage.getItem(USER_KEY);
    return userJson ? JSON.parse(userJson) : null;
  } catch (error) {
    console.error('Failed to retrieve user:', error);
    return null;
  }
}

/**
 * Clear JWT token and user data from localStorage
 */
export function clearToken(): void {
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  } catch (error) {
    console.error('Failed to clear token:', error);
  }
}

/**
 * Check if a valid token exists in localStorage
 */
export function hasToken(): boolean {
  return getToken() !== null;
}

/**
 * Decode JWT token to extract claims (basic decoding without verification)
 * WARNING: Only use for UI purposes. Always validate on backend.
 */
export function decodeToken(token: string): Record<string, unknown> | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const decoded = JSON.parse(atob(parts[1]));
    return decoded;
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
}

/**
 * Check if token is expired (frontend check only, backend validates)
 */
export function isTokenExpired(token: string): boolean {
  const decoded = decodeToken(token);
  if (!decoded || !decoded.exp) return true;

  const expirationTime = (decoded.exp as number) * 1000; // Convert to milliseconds
  return Date.now() >= expirationTime;
}
