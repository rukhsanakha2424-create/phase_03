/**
 * Authentication Form Validation
 * Email and password validation rules
 */

export interface ValidationError {
  field: string
  message: string
}

/**
 * Validate email format
 */
export function validateEmail(email: string): ValidationError | null {
  if (!email) {
    return { field: 'email', message: 'Email is required' }
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return { field: 'email', message: 'Please enter a valid email address' }
  }

  return null
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): ValidationError | null {
  if (!password) {
    return { field: 'password', message: 'Password is required' }
  }

  if (password.length < 8) {
    return {
      field: 'password',
      message: 'Password must be at least 8 characters long',
    }
  }

  return null
}

/**
 * Validate name (optional, but if provided, must be valid)
 */
export function validateName(name: string | undefined): ValidationError | null {
  if (!name) return null

  if (name.trim().length < 2) {
    return { field: 'name', message: 'Name must be at least 2 characters long' }
  }

  if (name.length > 100) {
    return { field: 'name', message: 'Name must not exceed 100 characters' }
  }

  return null
}

/**
 * Validate sign-up form
 */
export function validateSignUpForm(
  email: string,
  password: string,
  name?: string
): ValidationError | null {
  // Check email
  let error = validateEmail(email)
  if (error) return error

  // Check password
  error = validatePassword(password)
  if (error) return error

  // Check name if provided
  if (name) {
    error = validateName(name)
    if (error) return error
  }

  return null
}

/**
 * Validate sign-in form
 */
export function validateSignInForm(
  email: string,
  password: string
): ValidationError | null {
  // Check email
  let error = validateEmail(email)
  if (error) return error

  // Check password
  error = validatePassword(password)
  if (error) return error

  return null
}
