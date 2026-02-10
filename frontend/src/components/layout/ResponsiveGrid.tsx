/**
 * ResponsiveGrid Component
 * Responsive grid layout with flexible columns
 */

import React, { HTMLAttributes } from 'react'

interface ResponsiveGridProps extends HTMLAttributes<HTMLDivElement> {
  columns?: 1 | 2 | 3 | 4
  gap?: 'sm' | 'md' | 'lg'
}

export function ResponsiveGrid({
  columns = 1,
  gap = 'md',
  className = '',
  children,
  ...props
}: ResponsiveGridProps) {
  const columnClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 sm:grid-cols-2',
    3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
  }

  const gapClasses = {
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
  }

  return (
    <div
      className={`grid ${columnClasses[columns]} ${gapClasses[gap]} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
