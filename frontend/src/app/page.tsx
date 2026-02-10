/**
 * Home / Landing Page
 * Main entry point for unauthenticated users
 * Displays the landing page with product information
 */

import { LandingHeader } from '@/components/landing/LandingHeader'
import { Hero } from '@/components/landing/Hero'
import { Features } from '@/components/landing/Features'
import { ValueProp } from '@/components/landing/ValueProp'
import { LandingCTA } from '@/components/landing/LandingCTA'

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <LandingHeader />
      <Hero />
      <Features />
      <ValueProp />
      <LandingCTA />

      {/* Footer */}
      <footer className="bg-organify-primary py-8 px-4 sm:px-6 lg:px-8 border-t border-organify-primary-dark">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <p className="text-white text-sm">
              &copy; 2025 Organify. All rights reserved.
            </p>
            <div className="mt-4 flex gap-6 justify-center">
              <a href="/privacy" className="text-organify-neutral hover:text-white transition-colors text-sm">
                Privacy Policy
              </a>
              <a href="/terms" className="text-organify-neutral hover:text-white transition-colors text-sm">
                Terms of Service
              </a>
              <a href="/contact" className="text-organify-neutral hover:text-white transition-colors text-sm">
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
