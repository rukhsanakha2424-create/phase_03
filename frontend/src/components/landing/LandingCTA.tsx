/**
 * LandingCTA Component
 * Bold call-to-action section with contained rectangular gradient background
 * Inspired by modern SaaS landing pages with striking color and typography
 * Part of User Story 1: Landing Page
 */

import Link from "next/link";
import { Lock, Check } from "lucide-react";
import { Button } from "@/components/common/Button";

interface LandingCTAProps {
  headline?: string;
  headlineHighlight?: string;
  description?: string;
  primaryCtaText?: string;
  primaryCtaHref?: string;
  trustBadgeText?: string;
  freeText?: string;
}

export function LandingCTA({
  headline = "Ready to reclaim your",
  headlineHighlight = "time and find focus?",
  description = "Join 50,000+ high-achievers who have abandoned traditional planners.",
  primaryCtaText = "Try Organify for free",
  primaryCtaHref = "/signup",
  trustBadgeText = "Join 50,000+ users achieving more",
  freeText = "No credit card required",
}: LandingCTAProps) {
  return (
    <section className="relative py-24 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto bg-gradient-to-br from-organify-primary to-organify-secondary rounded-2xl lg:rounded-3xl py-20 sm:py-18 px-6 sm:px-8 lg:px-12 relative overflow-hidden">
        <div className="w-full max-w-3xl mx-auto text-center relative z-10">
          {/* Headline with highlight */}
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-white mb-8 tracking-tight leading-tight"
            style={{
              color: "#ffffff",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            {headline}
            <br />
            <span className="">{headlineHighlight}</span>
          </h2>

          {/* Description */}
          <p className="text-lg sm:text-xl text-white/90 mb-12 leading-relaxed max-w-2xl mx-auto">
            {description}
          </p>

          {/* Primary CTA Button - bold and prominent */}
          <div className="mb-12">
            <Link href={primaryCtaHref}>
              <Button
                variant="accent"
                size="lg"
                className="px-10 py-4 text-lg font-bold shadow-xl hover:shadow-2xl bg-organify-primary text-white hover:bg-organify-secondary transition-all duration-300 transform hover:scale-105"
              >
                {primaryCtaText}
              </Button>
            </Link>
          </div>

          {/* Trust indicators */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8 border-t border-white/20">
            {/* Badge 1 */}
            <div className="flex items-center gap-2">
              <Check color="#ffffff" strokeWidth={1.5} />
              <span className="text-white font-medium text-sm">
                {trustBadgeText}
              </span>
            </div>

            {/* Badge 2 */}
            <div className="flex items-center gap-2">
              <Lock color="#ffffff" strokeWidth={1.5} />
              <span className="text-white/90 font-medium text-sm">
                {freeText}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
