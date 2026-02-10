/**
 * ValueProp Component
 * Two feature cards showcasing product benefits with image placeholders
 * Inspired by modern SaaS landing pages showing practical use cases
 * Part of User Story 1: Landing Page
 */

import Link from "next/link";
import { Button } from "@/components/common/Button";

interface ValuePropProps {
  features?: Array<{
    title: string;
    description: string;
    imageSide?: "left" | "right";
    icon?: React.ReactNode;
  }>;
}

const FocusIcon = () => (
  <svg
    className="w-6 h-6"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M13 10V3L4 14h7v7l9-11h-7z"
    />
  </svg>
);

const ClockIcon = () => (
  <svg
    className="w-6 h-6"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 8v4l3 2m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
    />
  </svg>
);

export function ValueProp({
  features = [
    {
      title: "Focus Mode",
      description:
        "Eliminate distractions and concentrate on one task at a time with our minimalist interface designed for deep work.",
      imageSide: "right",
      icon: <FocusIcon />,
    },
    {
      title: "Smart Scheduling",
      description:
        "Our intelligent algorithm automatically adjusts your priorities based on deadlines and importance, ensuring you tackle the right tasks first.",
      imageSide: "left",
      icon: <ClockIcon />,
    },
  ],
}: ValuePropProps) {
  return (
    <section className="relative bg-background py-20 sm:py-32 px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Subtle background elements */}
      <div className="absolute top-1/4 -right-40 w-80 h-80 bg-organify-primary/3 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/4 -left-40 w-80 h-80 bg-organify-accent/3 rounded-full blur-3xl"></div>

      <div className="w-full max-w-7xl mx-auto relative z-10 space-y-24">
        {features.map((feature, index) => (
          <div
            key={index}
            className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center"
          >
            {/* Text Content */}
            <div
              className={`space-y-6 ${
                feature.imageSide === "left" ? "lg:order-2" : "lg:order-1"
              }`}
            >
              {/* Icon with accent */}
              <div className="flex items-center gap-4">
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-lg bg-gradient-to-br from-organify-accent to-organify-primary text-white">
                  {feature.icon}
                </div>
              </div>

              {/* Title and Description */}
              <div>
                <h3 className="text-3xl sm:text-4xl font-black text-slate mb-6 tracking-tight">
                  {feature.title}
                </h3>
                <p className="text-lg text-slate-light leading-relaxed max-w-lg">
                  {feature.description}
                </p>
              </div>

              {/* Call-to-action link */}
              <div>
                <Link
                  href="#"
                  className="inline-flex items-center gap-2 text-organify-primary font-semibold hover:text-organify-secondary transition-colors group"
                >
                  <Button variant="primary">Learn more</Button>
                </Link>
              </div>
            </div>

            {/* Image Placeholder */}
            <div
              className={`flex items-center justify-center ${
                feature.imageSide === "left" ? "lg:order-1" : "lg:order-2"
              }`}
            >
              <div className="relative w-full max-w-md">
                {/* Glow effect */}
                <div className="absolute -inset-6 bg-gradient-to-br from-organify-primary/20 to-organify-accent/20 rounded-3xl blur-2xl"></div>

                {/* Image placeholder with realistic styling */}
                <div className="relative bg-slate rounded-2xl overflow-hidden shadow-2xl border border-slate-light/30">
                  {/* Placeholder content - simulates real image */}
                  <div className="aspect-video bg-gradient-to-br from-slate-dark/50 to-slate/50 flex items-center justify-center relative overflow-hidden">
                    {/* Decorative elements */}
                    <div className="absolute inset-0 bg-gradient-to-br from-organify-primary/10 to-organify-accent/10"></div>

                    {/* Center icon */}
                    <div className="relative z-10 text-center">
                      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm mb-4">
                        {feature.icon && (
                          <div className="text-white opacity-60">
                            {feature.icon}
                          </div>
                        )}
                      </div>
                      <p className="text-white/70 text-sm font-medium">
                        {index === 0 ? "Notebook & Pen" : "Hand Writing"}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
