/**
 * useTasks Hook
 * Custom hook for managing task operations
 */

import { useState, useCallback } from 'react'
import { apiClient } from '@/lib/api/client'
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/api/types'

/**
 * Transform task from API (snake_case) to frontend (camelCase)
 */
function transformTask(task: any): Task {
  const normalizeTimestamp = (timestamp: any): string => {
    if (!timestamp) return new Date().toISOString()
    return timestamp
  }

  return {
    id: String(task.id),
    title: task.title,
    notes: task.notes,  // Changed from description to notes
    completed: task.completed,
    priority: task.priority,
    agentId: task.agent_id ? String(task.agent_id) : undefined,  // Map snake_case to camelCase
    createdAt: normalizeTimestamp(task.created_at),  // Map snake_case to camelCase
    updatedAt: normalizeTimestamp(task.updated_at),  // Map snake_case to camelCase
    completedAt: task.completed_at ? normalizeTimestamp(task.completed_at) : null,  // Map snake_case to camelCase
  }
}

export interface UseTasksResult {
  tasks: Task[]
  isLoading: boolean
  error: string | null
  fetchTasks: () => Promise<void>
  createTask: (data: CreateTaskRequest) => Promise<Task>
  updateTask: (taskId: string, data: UpdateTaskRequest) => Promise<Task>
  completeTask: (taskId: string) => Promise<Task>
  incompleteTask: (taskId: string) => Promise<Task>
  deleteTask: (taskId: string) => Promise<void>
  clearError: () => void
}

export function useTasks(): UseTasksResult {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const fetchTasks = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const taskData = await apiClient.get<any[]>(`/api/v1/todos`)
      setTasks(taskData.map(transformTask))
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch tasks'
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const createTask = useCallback(
    async (data: CreateTaskRequest): Promise<Task> => {
      setIsLoading(true)
      setError(null)
      try {
        // Transform request data to match backend expectations
        const requestData = {
          title: data.title,
          notes: data.notes,  // Send notes instead of description
          priority: data.priority || 'medium',
          agent_id: data.agentId ? parseInt(data.agentId) : null  // Convert to snake_case and number
        }
        const newTaskData = await apiClient.post<any>(`/api/v1/todos`, requestData)
        const newTask = transformTask(newTaskData)
        setTasks((prev) => [...prev, newTask])
        return newTask
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to create task'
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const updateTask = useCallback(
    async (taskId: string, data: UpdateTaskRequest): Promise<Task> => {
      setIsLoading(true)
      setError(null)
      try {
        // Transform request data to match backend expectations
        const requestData: any = {}
        if (data.title !== undefined) requestData.title = data.title
        if (data.notes !== undefined) requestData.notes = data.notes  // Send notes instead of description
        if (data.priority !== undefined) requestData.priority = data.priority
        if (data.completed !== undefined) requestData.completed = data.completed
        if (data.agentId !== undefined) requestData.agent_id = data.agentId ? parseInt(data.agentId) : null

        const updatedTaskData = await apiClient.patch<any>(
          `/api/v1/todos/${taskId}`,
          requestData
        )
        const updatedTask = transformTask(updatedTaskData)
        setTasks((prev) =>
          prev.map((task) => (task.id === taskId ? updatedTask : task))
        )
        return updatedTask
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to update task'
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const completeTask = useCallback(
    async (taskId: string): Promise<Task> => {
      setIsLoading(true)
      setError(null)
      try {
        const updatedTaskData = await apiClient.post<any>(
          `/api/v1/todos/${taskId}/toggle`
        )
        const updatedTask = transformTask(updatedTaskData)
        setTasks((prev) =>
          prev.map((task) => (task.id === taskId ? updatedTask : task))
        )
        return updatedTask
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to complete task'
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const incompleteTask = useCallback(
    async (taskId: string): Promise<Task> => {
      setIsLoading(true)
      setError(null)
      try {
        const updatedTaskData = await apiClient.post<any>(
          `/api/v1/todos/${taskId}/toggle`
        )
        const updatedTask = transformTask(updatedTaskData)
        setTasks((prev) =>
          prev.map((task) => (task.id === taskId ? updatedTask : task))
        )
        return updatedTask
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to mark task incomplete'
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const deleteTask = useCallback(
    async (taskId: string): Promise<void> => {
      setIsLoading(true)
      setError(null)
      try {
        await apiClient.delete(`/api/v1/todos/${taskId}`)
        setTasks((prev) => prev.filter((task) => task.id !== taskId))
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to delete task'
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    completeTask,
    incompleteTask,
    deleteTask,
    clearError,
  }
}