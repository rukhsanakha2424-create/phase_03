'use client'

import { getPriorityColor, getPriorityLabel, getPriorityIcon } from '@/lib/utils/priority'

/**
 * Get icon size based on badge size
 */
function getIconSize(size: 'sm' | 'md' | 'lg'): number {
  switch (size) {
    case 'sm':
      return 14
    case 'md':
      return 16
    case 'lg':
      return 20
    default:
      return 16
  }
}

/**
 * Props for the PriorityBadge component
 */
interface PriorityBadgeProps {
  /** Priority level: 'low', 'medium', or 'high' (defaults to 'medium') */
  priority?: string
  /** Badge size: 'sm' (small), 'md' (medium), 'lg' (large). Default: 'md' */
  size?: 'sm' | 'md' | 'lg'
  /** Whether to show the icon (!, –, ↓). Default: true */
  showIcon?: boolean
  /** Whether to show the text label (Low, Medium, High). Default: true */
  showText?: boolean
}

/**
 * PriorityBadge Component
 *
 * Displays a color-coded badge to indicate task priority with accessible design.
 *
 * Features:
 * - Color-coded by priority (High: red, Medium: violet, Low: slate)
 * - Includes icon for accessibility (not relying on color alone)
 * - Supports responsive sizing
 * - ARIA labels for screen readers
 *
 * @example
 * // Display medium priority badge
 * <PriorityBadge priority="medium" />
 *
 * @example
 * // Display small, icon-only badge
 * <PriorityBadge priority="high" size="sm" showText={false} />
 *
 * @example
 * // Display large badge with full label
 * <PriorityBadge priority="low" size="lg" showIcon={true} showText={true} />
 */
export function PriorityBadge({
  priority,
  size = 'md',
  showIcon = true,
  showText = true,
}: PriorityBadgeProps) {
  const color = getPriorityColor(priority)
  const label = getPriorityLabel(priority)
  const IconComponent = getPriorityIcon(priority)
  const iconSize = getIconSize(size)

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  return (
    <div
      className={`inline-flex items-center gap-1.5 rounded font-medium text-white ${sizeClasses[size]}`}
      style={{ backgroundColor: color }}
      title={label}
      role="badge"
      aria-label={`Priority: ${label}`}
    >
      {showIcon && <IconComponent size={iconSize} strokeWidth={2.5} />}
      {showText && <span>{label}</span>}
    </div>
  )
}
