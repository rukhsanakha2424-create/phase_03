'use client'

/**
 * Create Task Page
 * Form for creating new tasks
 */

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth/useAuth'
import { useTasks } from '@/lib/hooks/useTasks'
import { TaskForm } from '@/components/tasks/TaskForm'
import { CreateTaskRequest } from '@/lib/api/types'
import { Container } from '@/components/layout/Container'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'

export default function CreateTaskPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const { createTask, isLoading, error, clearError } = useTasks()
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isAuthenticated || !user?.id) {
    return null // Middleware should redirect to signin
  }

  const handleSubmit = async (data: CreateTaskRequest) => {
    setIsSubmitting(true)
    try {
      await createTask(data)
      // Redirect to tasks list on success
      router.push('/tasks')
    } catch {
      // Error is handled by the hook
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancel = () => {
    router.back()
  }

  if (isLoading && isSubmitting) {
    return <LoadingSpinner message="Creating task..." fullscreen />
  }

  return (
    <Container size="md" className="py-8">
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create Task</h1>
          <p className="mt-2 text-gray-600">Add a new task to your list</p>
        </div>

        <div className="rounded-lg bg-white p-8 shadow-sm border border-gray-200">
          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isLoading={isSubmitting}
            error={error}
            onErrorDismiss={clearError}
          />
        </div>
      </div>
    </Container>
  )
}
