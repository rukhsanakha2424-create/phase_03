/**
 * ErrorAlert Component
 * Displays error messages in a styled alert box
 */

import React from 'react'

interface ErrorAlertProps {
  message: string | null | undefined
  onDismiss?: () => void
  title?: string
}

export function ErrorAlert({ message, onDismiss, title }: ErrorAlertProps) {
  if (!message) return null

  return (
    <div className="rounded-lg bg-white p-4 border border-error/20">
      <div className="flex gap-3">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-error" viewBox="0 0 20 20" fill="currentColor">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        </div>

        <div className="flex-1">
          {title && <p className="font-medium text-error">{title}</p>}
          <p className={`text-sm text-error ${title ? 'mt-1' : ''}`}>{message}</p>
        </div>

        {onDismiss && (
          <button
            onClick={onDismiss}
            className="flex-shrink-0 text-error hover:text-errorLight"
            aria-label="Dismiss"
          >
            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  )
}
