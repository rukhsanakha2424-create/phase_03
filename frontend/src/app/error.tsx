'use client'

/**
 * Global Error Boundary
 * Handles errors in the application
 */

'use client'

import { useEffect } from 'react'
import { Button } from '@/components/common/Button'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to monitoring service
    console.error('Application error:', error)
  }, [error])

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 py-12">
      <div className="w-full max-w-md space-y-8 text-center">
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Oops!</h1>
          <p className="mt-2 text-gray-600">Something went wrong</p>
        </div>

        <div className="rounded-lg bg-red-50 p-4 border border-red-200">
          <p className="text-sm text-red-700">{error.message || 'An unexpected error occurred'}</p>
        </div>

        <div className="flex gap-3">
          <Button onClick={reset} className="flex-1">
            Try Again
          </Button>
          <Button
            variant="secondary"
            onClick={() => {
              window.location.href = '/'
            }}
            className="flex-1"
          >
            Go Home
          </Button>
        </div>
      </div>
    </div>
  )
}
