'use client'

/**
 * Sign In Page
 * User authentication page
 */

import { useState } from 'react'
import { SignInForm } from '@/components/auth/SignInForm'
import { useAuth } from '@/lib/auth/useAuth'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'

export default function SignInPage() {
  const { signIn, isLoading, error, clearError } = useAuth()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (email: string, password: string) => {
    setIsSubmitting(true)
    try {
      await signIn(email, password)
      // Redirect is handled by auth context
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <LoadingSpinner message="Signing in..." fullscreen />
  }

  return (
    <div>
      <SignInForm
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
        error={error?.message || null}
        onErrorDismiss={clearError}
      />
    </div>
  )
}
