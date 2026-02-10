/**
 * Better Auth Configuration
 * Minimal configuration for JWT-based authentication
 *
 * NOTE: This app uses a custom backend authentication implementation:
 * - Signup: POST /auth/signup
 * - Signin: POST /auth/signin
 * - Signout: POST /auth/signout
 *
 * JWT tokens are managed via:
 * - Storage: localStorage (jwt-storage.ts)
 * - Injection: API client adds Authorization header (api/client.ts)
 * - Validation: Backend validates JWT on protected endpoints
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export const authConfig = {
  apiBaseUrl: API_BASE_URL,
  endpoints: {
    signup: `${API_BASE_URL}/auth/signup`,
    signin: `${API_BASE_URL}/auth/signin`,
    signout: `${API_BASE_URL}/auth/signout`,
  },
  tokenConfig: {
    expirationDays: 7,
    storageKey: 'auth_token',
  },
  redirects: {
    afterSignin: '/tasks',
    afterSignup: '/tasks',
    afterSignout: '/signin',
    unauthorized: '/signin',
  },
}

export type AuthConfig = typeof authConfig
