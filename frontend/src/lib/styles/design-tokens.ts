/**
 * Design Tokens for Todo Application
 *
 * This file defines the complete design system including colors, spacing,
 * typography, and breakpoints. All tokens are derived from frontend/design-guide.md
 * and should be used consistently throughout the application.
 *
 * @see {@link ../../../design-guide.md} Design Guide
 */

/**
 * Color Palette
 * Based on design-guide.md with semantic naming for usage context
 */
export const colors = {
  // Primary Structure (60-70% of interface)
  slate: '#323843',     // Midnight Slate - backgrounds, structure
  slateLight: '#3d444f', // Lighter variant for hover states
  slateDark: '#252a31',  // Darker variant for shadows

  // Primary Action (accent color)
  violet: '#9e90ac',    // Focus Violet - buttons, active states, links
  violetLight: '#de94dc', // Lighter variant for hover
  violetDark: '#dcaede', // Darker variant for active

  // Success/Progress
  lime: '#cbe857',      // Momentum Lime - success states, completed tasks
  limeDark: '#b3d946',  // Darker variant

  // Text & Contrast (readability)
  white: '#f5f5f5',     // Paper White - text, contrast

  // Status/Semantic colors
  error: '#ff6b6b',     // Error/destructive actions
  errorLight: '#ff8c8c', // Error hover state
  warning: '#ffd43b',   // Warning states
  success: '#cbe857',   // Success (alias for lime)
} as const;

/**
 * Spacing Scale
 * Used for padding, margins, gaps, and sizing
 * Follows a 4px base grid
 */
export const spacing = {
  xs: '4px',    // 0.25rem
  sm: '8px',    // 0.5rem
  md: '12px',   // 0.75rem
  base: '16px', // 1rem (default)
  lg: '24px',   // 1.5rem
  xl: '32px',   // 2rem
  '2xl': '48px', // 3rem
  // Numeric aliases for Tailwind integration
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  6: '24px',
  8: '32px',
  12: '48px',
} as const;

/**
 * Typography Scale
 * Defines font sizes, weights, and line heights for text hierarchy
 */
export const typography = {
  // Heading styles
  h1: {
    size: '32px',
    weight: 600,
    lineHeight: '1.2',
  },
  h2: {
    size: '24px',
    weight: 600,
    lineHeight: '1.3',
  },
  h3: {
    size: '18px',
    weight: 600,
    lineHeight: '1.4',
  },
  // Body text
  body: {
    size: '16px',
    weight: 400,
    lineHeight: '1.5',
  },
  small: {
    size: '14px',
    weight: 400,
    lineHeight: '1.5',
  },
  caption: {
    size: '12px',
    weight: 400,
    lineHeight: '1.4',
  },
} as const;

/**
 * Responsive Breakpoints
 * Mobile-first approach: base styles for mobile, media queries for larger screens
 */
export const breakpoints = {
  xs: '0px',     // Extra small (mobile)
  sm: '320px',   // Small (mobile)
  md: '768px',   // Medium (tablet)
  lg: '1024px',  // Large (desktop)
  xl: '1280px',  // Extra large (wide desktop)
  '2xl': '1536px', // 2x large (ultra-wide)
} as const;

/**
 * Z-index Scale
 * For managing stacking context
 */
export const zIndex = {
  hide: -1,
  base: 0,
  dropdown: 1000,
  fixed: 1020,
  modal: 1040,
  popover: 1050,
  tooltip: 1060,
} as const;

/**
 * Border Radius Scale
 * For consistent corner rounding
 */
export const borderRadius = {
  none: '0',
  sm: '4px',
  base: '8px',
  md: '12px',
  lg: '16px',
  full: '9999px',
} as const;

/**
 * Shadow Scale
 * For depth and elevation
 */
export const shadows = {
  none: 'none',
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  md: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  lg: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  xl: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
} as const;

/**
 * Transition/Animation durations
 * For consistent motion timing
 */
export const transitions = {
  fast: '150ms',
  base: '200ms',
  slow: '300ms',
  slowest: '500ms',
} as const;

/**
 * Accessibility - Reduced Motion
 * Query for prefers-reduced-motion
 */
export const a11y = {
  prefersReducedMotion: '@media (prefers-reduced-motion: reduce)',
} as const;

/**
 * Utility: Get spacing value
 * Converts numeric or string spacing keys to pixel values
 */
export function getSpacing(key: keyof typeof spacing | number): string {
  if (typeof key === 'number') {
    return `${key * 4}px`;
  }
  return spacing[key];
}

/**
 * Utility: Get color value
 */
export function getColor(key: keyof typeof colors): string {
  return colors[key];
}

/**
 * Utility: Check if prefers-reduced-motion
 */
export function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Export all tokens as default for Tailwind integration
 */
export default {
  colors,
  spacing,
  typography,
  breakpoints,
  zIndex,
  borderRadius,
  shadows,
  transitions,
  a11y,
};
