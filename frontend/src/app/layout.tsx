import type { Metadata } from 'next'
import { Space_Grotesk, Roboto } from 'next/font/google'
import { AuthProvider } from '@/lib/auth/auth-context'
import '@/styles/globals.css'

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  weight: ['400', '500', '600', '700'],
})

const roboto = Roboto({
  subsets: ['latin'],
  variable: '--font-roboto',
  weight: ['400', '500', '700'],
})

export const metadata: Metadata = {
  title: 'Organify- Todo App',
  description: 'A modern todo application for task management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${spaceGrotesk.className} ${roboto.className}`}>
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  )
}
