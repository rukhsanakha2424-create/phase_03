/**
 * TaskList Component
 * Displays array of tasks with optional grouping by completion status
 */

import React from 'react'
import { CheckCircle2 } from 'lucide-react'
import { Task } from '@/lib/api/types'
import { TaskItem } from './TaskItem'

interface TaskListProps {
  tasks: Task[]
  onEdit?: (taskId: string) => void
  onDelete?: (taskId: string) => Promise<void>
  onComplete?: (taskId: string) => Promise<void>
  isLoading?: boolean
}

export function TaskList({
  tasks,
  onEdit,
  onDelete,
  onComplete,
  isLoading = false,
}: TaskListProps) {
  if (tasks.length === 0) {
    return null
  }

  // Separate completed and incomplete tasks
  const incompleteTasks = tasks.filter((task) => !task.completed)
  const completedTasks = tasks.filter((task) => task.completed)

  return (
    <div className="space-y-6">
      {/* Incomplete Tasks Section */}
      {incompleteTasks.length > 0 && (
        <div>
          <div className="mb-3 flex items-center gap-2">
            <h2 className="text-sm font-semibold text-slate-light uppercase tracking-wide">
              Active Tasks
            </h2>
            <span className="rounded-full bg-organify-primary/20 px-2 py-0.5 text-xs font-medium text-organify-primary">
              {incompleteTasks.length}
            </span>
          </div>
          <div className="space-y-3">
            {incompleteTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={onEdit}
                onDelete={onDelete}
                onComplete={onComplete}
                isLoading={isLoading}
              />
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks Section */}
      {completedTasks.length > 0 && (
        <div>
          <div className="mb-3 flex items-center gap-2">
            <h2 className="text-sm font-semibold text-slate-light uppercase tracking-wide">
              Completed
            </h2>
            <span className="rounded-full bg-success/20 px-2 py-0.5 text-xs font-medium text-success">
              {completedTasks.length}
            </span>
          </div>
          <div className="space-y-3">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={onEdit}
                onDelete={onDelete}
                onComplete={onComplete}
                isLoading={isLoading}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
