'use client'

import { PRIORITY_OPTIONS } from '@/lib/utils/priority'

/**
 * Props for the PrioritySelector component
 */
interface PrioritySelectorProps {
  /** Current priority value ('low', 'medium', or 'high'). Default: 'medium' */
  value?: string
  /** Callback function when priority selection changes */
  onChange: (value: string) => void
  /** Label text for the select element. Default: 'Priority' */
  label?: string
  /** Whether the field is required. Default: false */
  required?: boolean
  /** Whether the select is disabled. Default: false */
  disabled?: boolean
}

/**
 * PrioritySelector Component
 *
 * A dropdown select component for choosing task priority levels.
 *
 * Features:
 * - Offers three options: Low, Medium (default), High
 * - Fully accessible with labels and ARIA attributes
 * - Keyboard navigable
 * - Responsive design
 * - Controlled component pattern
 *
 * @example
 * // Basic usage
 * const [priority, setPriority] = useState('medium')
 * <PrioritySelector value={priority} onChange={setPriority} />
 *
 * @example
 * // With label and required
 * <PrioritySelector
 *   value={priority}
 *   onChange={setPriority}
 *   label="Task Priority *"
 *   required={true}
 * />
 *
 * @example
 * // Disabled state
 * <PrioritySelector
 *   value={priority}
 *   onChange={setPriority}
 *   disabled={isLoading}
 * />
 */
export function PrioritySelector({
  value = 'medium',
  onChange,
  label = 'Priority',
  required = false,
  disabled = false,
}: PrioritySelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="priority-select" className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <select
        id="priority-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
      >
        {PRIORITY_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )
}
