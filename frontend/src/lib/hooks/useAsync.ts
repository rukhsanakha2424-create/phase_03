'use client'

/**
 * useAsync Hook
 * Custom hook for managing async operations
 */

import { useState, useCallback } from 'react'

export interface AsyncState<T> {
  status: 'idle' | 'pending' | 'success' | 'error'
  data: T | null
  error: Error | null
}

export interface UseAsyncResult<T> extends AsyncState<T> {
  execute: () => Promise<void>
  retry: () => Promise<void>
  reset: () => void
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
): UseAsyncResult<T> {
  const [state, setState] = useState<AsyncState<T>>({
    status: 'idle',
    data: null,
    error: null,
  })

  // Execute the async function
  const execute = useCallback(async () => {
    setState({ status: 'pending', data: null, error: null })
    try {
      const response = await asyncFunction()
      setState({ status: 'success', data: response, error: null })
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error))
      setState({ status: 'error', data: null, error: err })
      throw err
    }
  }, [asyncFunction])

  // Retry the async function
  const retry = useCallback(async () => {
    await execute()
  }, [execute])

  // Reset the state
  const reset = useCallback(() => {
    setState({ status: 'idle', data: null, error: null })
  }, [])

  // Execute immediately if requested
  useState(() => {
    if (immediate) {
      execute()
    }
  })

  return {
    ...state,
    execute,
    retry,
    reset,
  }
}
