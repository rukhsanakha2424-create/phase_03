/**
 * Centralized API Client
 * Handles all HTTP requests with automatic JWT injection
 * Implements 401 error handling and consistent error serialization
 */

import { AuthError, ApiResponse } from './types'
import { getToken, clearToken } from '@/lib/auth/jwt-storage'

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

interface FetchOptions extends RequestInit {
  skipAuth?: boolean
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = BASE_URL) {
    this.baseUrl = baseUrl
  }

  /**
   * Get JWT token from localStorage and create Authorization header
   */
  private getAuthHeader(): string | null {
    try {
      const token = getToken()
      if (token) {
        return `Bearer ${token}`
      }
      return null
    } catch {
      return null
    }
  }

  /**
   * Handle API response
   * Parses JSON and handles error cases
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('content-type')
    let data: unknown

    if (contentType?.includes('application/json')) {
      data = await response.json()
    } else {
      data = await response.text()
    }

    // Handle 401 - Clear token and redirect to signin
    if (response.status === 401) {
      clearToken()
      if (typeof window !== 'undefined') {
        window.location.href = '/signin'
      }
      const error: AuthError = {
        code: 'UNAUTHORIZED',
        message: 'Session expired. Please sign in again.',
      }
      throw error
    }

    // Handle other error status codes
    if (!response.ok) {
      let error: AuthError
      if (typeof data === 'object' && data !== null && 'detail' in data) {
        error = {
          code: `HTTP_${response.status}`,
          message: (data as Record<string, unknown>).detail as string,
        }
      } else {
        error = {
          code: `HTTP_${response.status}`,
          message: typeof data === 'string' ? data : 'An error occurred',
        }
      }
      throw error
    }

    return data as T
  }

  /**
   * Make GET request
   */
  async get<T = unknown>(path: string, options?: FetchOptions): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    }

    // Add Authorization header if token exists
    const authHeader = this.getAuthHeader()
    if (authHeader) {
      (headers as Record<string, string>)['Authorization'] = authHeader
    }

    const response = await fetch(url, {
      ...options,
      method: 'GET',
      headers,
    })

    return this.handleResponse<T>(response)
  }

  /**
   * Make POST request
   */
  async post<T = unknown>(
    path: string,
    body?: unknown,
    options?: FetchOptions
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    }

    // Add Authorization header if token exists
    const authHeader = this.getAuthHeader()
    if (authHeader) {
      (headers as Record<string, string>)['Authorization'] = authHeader
    }

    const response = await fetch(url, {
      ...options,
      method: 'POST',
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })

    return this.handleResponse<T>(response)
  }

  /**
   * Make PUT request
   */
  async put<T = unknown>(
    path: string,
    body?: unknown,
    options?: FetchOptions
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    }

    // Add Authorization header if token exists
    const authHeader = this.getAuthHeader()
    if (authHeader) {
      (headers as Record<string, string>)['Authorization'] = authHeader
    }

    const response = await fetch(url, {
      ...options,
      method: 'PUT',
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })

    return this.handleResponse<T>(response)
  }

  /**
   * Make PATCH request
   */
  async patch<T = unknown>(
    path: string,
    body?: unknown,
    options?: FetchOptions
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    }

    // Add Authorization header if token exists
    const authHeader = this.getAuthHeader()
    if (authHeader) {
      (headers as Record<string, string>)['Authorization'] = authHeader
    }

    const response = await fetch(url, {
      ...options,
      method: 'PATCH',
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })

    return this.handleResponse<T>(response)
  }

  /**
   * Make DELETE request
   */
  async delete<T = unknown>(path: string, options?: FetchOptions): Promise<T> {
    const url = `${this.baseUrl}${path}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options?.headers,
    }

    // Add Authorization header if token exists
    const authHeader = this.getAuthHeader()
    if (authHeader) {
      (headers as Record<string, string>)['Authorization'] = authHeader
    }

    const response = await fetch(url, {
      ...options,
      method: 'DELETE',
      headers,
    })

    return this.handleResponse<T>(response)
  }
}

// Export singleton instance
export const apiClient = new ApiClient()
