/**
 * Hero Component
 * Main hero section for landing page with headline, subheadline, and CTA
 * Part of User Story 1: Landing Page
 */

import { Button } from "@/components/common/Button";
import Link from "next/link";

interface HeroProps {
  headline?: string;
  subheadline?: string;
  ctaText?: string;
  ctaHref?: string;
  secondaryCtaText?: string;
  secondaryCtaHref?: string;
}

export function Hero({
  headline = "Simplify Work. Amplify Results.",
  subheadline = "A modern, intuitive todo application designed for productivity and clarity",
  ctaText = "Get Started Free",
  ctaHref = "/signup",
  secondaryCtaText = "Learn More",
  secondaryCtaHref = "#features",
}: HeroProps) {
  return (
    <section
      className="relative min-h-screen flex flex-col items-center justify-center px-4 py-16 overflow-hidden"
      style={{ backgroundColor: "#f0f2f5" }}
    >
      <div
        className="absolute top-20 right-10 w-72 h-72 rounded-full blur-3xl opacity-40"
        style={{ backgroundColor: "#4361ee" }}
      ></div>
      <div
        className="absolute bottom-32 left-10 w-80 h-80 rounded-full blur-3xl opacity-40"
        style={{ backgroundColor: "#4cc9f0" }}
      ></div>

      <div className="w-full max-w-4xl space-y-6 text-center relative z-10">
        {/* Decorative badge with accent color */}
        <div className="flex items-center justify-center gap-2">
          <div
            className="h-[2px] w-6 rounded-full"
            style={{ backgroundColor: "#4361ee" }}
          ></div>
          <span
            className="text-sm font-semibold tracking-wider uppercase"
            style={{ color: "#4361ee" }}
          >
            Tasks Made Simple
          </span>
          <div
            className="h-[2px] w-6 rounded-full"
            style={{ backgroundColor: "#4361ee" }}
          ></div>
        </div>

        <div className="space-y-6">
          <h1
            className="text-5xl sm:text-6xl lg:text-8xl font-semibold leading-tight tracking-tighter"
            style={{
              color: "#343a40",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            {headline}
          </h1>

          {/* Subheadline with muted slate */}
          <p
            className="text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed font-light"
            style={{ color: "#343a40", opacity: 0.7 }}
          >
            {subheadline}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4 items-center">
          <Link href={ctaHref}>
            <Button
              variant="primary"
              className="text-sm font-semibold shadow-lg hover:shadow-xl"
            >
              {ctaText}
            </Button>
          </Link>
          <Link
            href={secondaryCtaHref}
            className="group flex items-center gap-2 font-semibold transition-all text-base"
            style={{ color: "#343a40" }}
          >
            <Button variant="secondary">{secondaryCtaText}</Button>
          </Link>
        </div>

        <div className="pt-12 mx-auto max-w-4xl">
          <div
            className="relative rounded-3xl shadow-2xl overflow-hidden border-4"
            style={{ borderColor: "#4361ee", backgroundColor: "#ffffff" }}
          >
            {/* Mock app UI */}
            <div className="p-8 space-y-6">
              <div className="flex gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: "#e63946" }}
                ></div>
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: "#4cc9f0" }}
                ></div>
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: "#fca311", opacity: 0.3 }}
                ></div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div
                    className="w-5 h-5 rounded-lg flex-shrink-0"
                    style={{ backgroundColor: "#4cc9f0" }}
                  ></div>
                  <div
                    className="h-3 rounded-full flex-grow"
                    style={{ backgroundColor: "#f0f2f5" }}
                  ></div>
                </div>
                <div className="flex items-center gap-3">
                  <div
                    className="w-5 h-5 rounded-lg flex-shrink-0"
                    style={{ backgroundColor: "#4361ee", opacity: 0.5 }}
                  ></div>
                  <div
                    className="h-3 rounded-full flex-grow"
                    style={{ backgroundColor: "#f0f2f5" }}
                  ></div>
                </div>
                <div className="flex items-center gap-3">
                  <div
                    className="w-5 h-5 rounded-lg flex-shrink-0"
                    style={{ backgroundColor: "#343a40", opacity: 0.2 }}
                  ></div>
                  <div
                    className="h-3 rounded-full flex-grow"
                    style={{ backgroundColor: "#f0f2f5" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
