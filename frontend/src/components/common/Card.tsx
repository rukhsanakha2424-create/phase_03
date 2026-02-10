/**
 * Card Component
 * Reusable card container with design system styling
 */

import React, { ReactNode, HTMLAttributes } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  hoverable?: boolean
  padding?: 'sm' | 'md' | 'lg'
}

export function Card({
  children,
  hoverable = false,
  padding = 'md',
  className = '',
  ...props
}: CardProps) {
  const paddingClasses = {
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8',
  }

  const baseClasses = `bg-white rounded-md border border-slate-light shadow-md ${paddingClasses[padding]}`
  const hoverClasses = hoverable ? 'transition-shadow duration-200 hover:shadow-lg' : ''

  return (
    <div
      className={`${baseClasses} ${hoverClasses} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
