/**
 * Next.js Middleware
 * Implements route protection and authentication flow
 *
 * Note: Route protection is primarily handled by:
 * 1. API client checks for JWT token and includes Authorization header
 * 2. API returns 401 Unauthorized if token is missing/invalid
 * 3. API client redirects to /signin on 401
 *
 * Since JWT is stored in localStorage (client-side), it cannot be read in middleware.
 * Therefore, protection is enforced at the API level.
 */

import { NextRequest, NextResponse } from 'next/server'

// Routes that don't require authentication
const publicRoutes = ['/signin', '/signup', '/']

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Check if route is public
  const isPublicRoute = publicRoutes.some((route) => {
    if (route === '/') {
      return pathname === '/'
    }
    return pathname.startsWith(route)
  })

  // Protected routes will be handled by API protection
  // When pages load, they make API calls which include JWT token
  // If token is missing, API returns 401 and client redirects to signin

  return NextResponse.next()
}

// Apply middleware to specific routes
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
}
