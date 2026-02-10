/**
 * Landing Page
 * Public landing page for unauthenticated users
 * Modern, professional design inspired by leading SaaS companies
 * Part of User Story 1: Landing Page
 */

import { LandingHeader } from '@/components/landing/LandingHeader'
import { Hero } from '@/components/landing/Hero'
import { Features } from '@/components/landing/Features'
import { ValueProp } from '@/components/landing/ValueProp'
import { LandingCTA } from '@/components/landing/LandingCTA'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <LandingHeader />
      <Hero />
      <Features />
      <ValueProp />
      <LandingCTA />

      {/* Footer */}
      <footer className="bg-slate-dark border-t border-slate-light/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 mb-12">
            {/* Brand */}
            <div>
              <h3 className="text-lg font-bold text-white mb-4">Tasks</h3>
              <p className="text-slate-light/70 text-sm leading-relaxed">
                Modern task management designed for focus and productivity.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wide">Product</h4>
              <ul className="space-y-3">
                <li>
                  <a href="#features" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#pricing" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Pricing
                  </a>
                </li>
                <li>
                  <a href="#" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Roadmap
                  </a>
                </li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wide">Company</h4>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Contact
                  </a>
                </li>
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wide">Legal</h4>
              <ul className="space-y-3">
                <li>
                  <a href="/privacy" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Privacy
                  </a>
                </li>
                <li>
                  <a href="/terms" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Terms
                  </a>
                </li>
                <li>
                  <a href="#" className="text-slate-light/70 hover:text-violet text-sm transition-colors">
                    Security
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom section with copyright and social */}
          <div className="border-t border-slate-light/10 pt-8">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <p className="text-slate-light/60 text-sm">
                &copy; 2025 Tasks. All rights reserved.
              </p>
              <div className="flex items-center gap-4">
                <a href="#" className="text-slate-light/70 hover:text-violet transition-colors">
                  <span className="sr-only">Twitter</span>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="text-slate-light/70 hover:text-violet transition-colors">
                  <span className="sr-only">GitHub</span>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.603-3.369-1.343-3.369-1.343-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.544 2.914 1.19.092-.926.35-1.544.636-1.9-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.268.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0110 4.817a9.54 9.54 0 012.502.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.379.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C17.138 18.194 20 14.44 20 10.017 20 4.484 15.522 0 10 0z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
