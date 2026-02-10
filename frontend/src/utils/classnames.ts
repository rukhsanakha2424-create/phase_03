/**
 * Classnames Utility
 * Conditionally combine CSS classes
 */

export type ClassValue = string | undefined | null | boolean | Record<string, boolean>

export function classnames(...classes: ClassValue[]): string {
  return classes
    .flatMap((cls) => {
      if (typeof cls === 'string') {
        return cls
      }
      if (typeof cls === 'object' && cls !== null) {
        return Object.entries(cls)
          .filter(([, value]) => value)
          .map(([key]) => key)
      }
      return []
    })
    .filter(Boolean)
    .join(' ')
}

// Alias
export const cn = classnames
