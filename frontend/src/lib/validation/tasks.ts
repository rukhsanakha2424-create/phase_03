/**
 * Task Form Validation
 * Title and notes validation rules
 */

export interface ValidationError {
  field: string
  message: string
}

/**
 * Validate task title
 */
export function validateTaskTitle(title: string): ValidationError | null {
  if (!title || !title.trim()) {
    return { field: 'title', message: 'Task title is required' }
  }

  if (title.trim().length < 3) {
    return {
      field: 'title',
      message: 'Task title must be at least 3 characters long',
    }
  }

  if (title.length > 200) {
    return {
      field: 'title',
      message: 'Task title must not exceed 200 characters',
    }
  }

  return null
}

/**
 * Validate task notes (optional)
 */
export function validateTaskNotes(
  notes: string | undefined
): ValidationError | null {
  if (!notes) return null

  if (notes.length > 1000) {
    return {
      field: 'notes',
      message: 'Task notes must not exceed 1000 characters',
    }
  }

  return null
}

/**
 * Validate task creation form
 */
export function validateTaskForm(
  title: string,
  notes?: string
): ValidationError | null {
  // Check title
  let error = validateTaskTitle(title)
  if (error) return error

  // Check notes if provided
  if (notes) {
    error = validateTaskNotes(notes)
    if (error) return error
  }

  return null
}
