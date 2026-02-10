'use client'

/**
 * Edit Task Page
 * Form for editing existing tasks
 */

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/lib/auth/useAuth'
import { useTasks } from '@/lib/hooks/useTasks'
import { TaskForm } from '@/components/tasks/TaskForm'
import { CreateTaskRequest, Task } from '@/lib/api/types'
import { Container } from '@/components/layout/Container'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorAlert } from '@/components/common/ErrorAlert'
import { apiClient } from '@/lib/api/client'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = params.taskId as string
  const { user, isAuthenticated } = useAuth()
  const { updateTask, isLoading, error, clearError } = useTasks()
  const [task, setTask] = useState<Task | null>(null)
  const [isLoadingTask, setIsLoadingTask] = useState(true)
  const [taskError, setTaskError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Fetch task on mount
  useEffect(() => {
    if (!isAuthenticated || !user?.id) {
      return
    }

    const loadTask = async () => {
      setIsLoadingTask(true)
      try {
        const data = await apiClient.get<Task>(`/api/v1/todos/${taskId}`)
        setTask(data)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load task'
        setTaskError(message)
      } finally {
        setIsLoadingTask(false)
      }
    }

    loadTask()
  }, [isAuthenticated, user?.id, taskId])

  if (!isAuthenticated || !user?.id) {
    return null // Middleware should redirect to signin
  }

  if (isLoadingTask) {
    return <LoadingSpinner message="Loading task..." fullscreen />
  }

  if (taskError || !task) {
    return (
      <Container size="md" className="py-8">
        <ErrorAlert
          message={taskError || 'Task not found'}
          title="Failed to load task"
        />
        <button
          onClick={() => router.push('/tasks')}
          className="mt-4 text-blue-600 hover:text-blue-700"
        >
          ← Back to tasks
        </button>
      </Container>
    )
  }

  const handleSubmit = async (data: CreateTaskRequest) => {
    setIsSubmitting(true)
    try {
      await updateTask(taskId, data)
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
    return <LoadingSpinner message="Updating task..." fullscreen />
  }

  return (
    <Container size="md" className="py-8">
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
          <p className="mt-2 text-gray-600">Update your task</p>
        </div>

        <div className="rounded-lg bg-white p-8 shadow-sm border border-gray-200">
          <TaskForm
            initialTask={task}
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
