'use client'

/**
 * useAuth Hook
 * Custom hook to access auth context from any component
 * Provides type-safe access to authentication state and functions
 */

import { useContext } from 'react'
import { AuthContext, AuthContextType } from './auth-context'

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}
