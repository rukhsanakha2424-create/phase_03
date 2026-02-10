/**
 * EmptyState Component
 * "No tasks yet" message with create button
 */

import React from 'react'
import Link from 'next/link'
import { Button } from '@/components/common/Button'

interface EmptyStateProps {
  onCreateClick?: () => void
}

export function EmptyState({ onCreateClick }: EmptyStateProps) {
  return (
    <div className="rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 py-12 px-4 text-center">
      <svg
        className="mx-auto h-12 w-12 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
        />
      </svg>

      <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
      <p className="mt-2 text-sm text-gray-600">
        Get started by creating you new task
      </p>

      <div className="mt-6">
        {onCreateClick ? (
          <Button onClick={onCreateClick}>Create Task</Button>
        ) : (
          <Link href="/tasks/new">
            <Button>Create Task</Button>
          </Link>
        )}
      </div>
    </div>
  )
}
