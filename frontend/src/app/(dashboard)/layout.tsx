/**
 * Dashboard Layout
 * Layout for authenticated pages with navbar
 */

import { ReactNode } from 'react'
import { Navbar } from '@/components/common/Navbar'

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <main className="py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  )
}
