/**
 * API Response Types
 * Shared types for all API responses
 */

export interface User {
  id: string
  email: string
  name?: string
  createdAt?: string
  updatedAt?: string
}

export interface Task {
  id: string
  title: string
  notes?: string  // Changed from description to notes
  completed: boolean
  priority?: string  // "low", "medium", or "high"
  agentId?: string  // Added agent association
  createdAt: string  // Changed from created_at to camelCase
  updatedAt: string  // Changed from updated_at to camelCase
  completedAt?: string | null  // Changed from completed_at to camelCase
}

export interface AuthError {
  code: string
  message: string
  details?: Record<string, unknown>
}

export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  error?: AuthError
}

export interface TaskListResponse {
  tasks: Task[]
  total: number
  page: number
  pageSize: number
}

export interface CreateTaskRequest {
  title: string
  notes?: string  // Changed from description to notes
  priority?: string  // "low", "medium", or "high"
  agentId?: string  // Added agent association
}

export interface UpdateTaskRequest {
  title?: string
  notes?: string  // Changed from description to notes
  completed?: boolean
  priority?: string  // "low", "medium", or "high"
  agentId?: string  // Added agent association
}

export interface SignUpRequest {
  email: string
  password: string
  name?: string
}

export interface SignInRequest {
  email: string
  password: string
}

export interface AuthResponse {
  user: User
  token: string
  expiresAt?: string
}
