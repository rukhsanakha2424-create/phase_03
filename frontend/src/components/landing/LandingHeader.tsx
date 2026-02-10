"use client";

/**
 * LandingHeader Component
 * Modern navigation header with mobile menu and enhanced interactions
 * Part of User Story 1: Landing Page
 */

import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/common/Button";
import { Menu, X } from "lucide-react";
import { useState } from "react";

interface LandingHeaderProps {
  brandName?: string;
  navLinks?: Array<{ label: string; href: string }>;
}

export function LandingHeader({
  brandName = "Organify",
  navLinks = [
    { label: "Product", href: "#features" },
    { label: "Workflow", href: "#workflow" },
    { label: "Pricing", href: "#pricing" },
  ],
}: LandingHeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-organify-primary/20">
      <nav className="px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between max-w-7xl mx-auto">
          {/* Brand/Logo */}
          <Link href="/" className="group flex items-center gap-3">
            <Image
              src="/assets/images.jpg"
              alt="Organify Logo"
              width={60}
              height={60}
              className="w-10 h-10 shadow-md rounded"
              
              priority
            />
            <span
              className="text-xl font-bold hidden sm:block"
              style={{
                color: "#343a40",
                fontFamily: "'Space Grotesk', sans-serif",
              }}
            >
              😊 {brandName}
            </span>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden lg:flex lg:items-center lg:gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-slate-light hover:text-organify-primary font-medium text-sm transition-colors duration-200 relative group"
              >
                {link.label}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-organify-primary to-organify-secondary group-hover:w-full transition-all duration-300" />
              </Link>
            ))}
          </div>

          {/* Desktop CTA Buttons */}
          <div className="hidden sm:flex items-center gap-3">
            <Link href="/signin">
              <Button variant="secondary" size="sm">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="primary" size="sm">
                Get Started
              </Button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="lg:hidden p-2 rounded-lg hover:bg-organify-primary/10 transition-colors"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? (
              <X size={24} className="text-organify-primary" />
            ) : (
              <Menu size={24} className="text-organify-primary" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden border-t border-organify-primary/20 bg-background/50 backdrop-blur-lg">
            <div className="px-4 py-6 space-y-4">
              {/* Mobile Navigation Links */}
              <div className="space-y-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setIsMenuOpen(false)}
                    className="block px-3 py-2 rounded-lg text-slate-light hover:bg-organify-primary/10 hover:text-organify-primary font-medium transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                ))}
              </div>

              {/* Mobile CTA Buttons */}
              <div className="border-t border-organify-primary/20 pt-4 space-y-2">
                <Link href="/signin" className="block">
                  <Button variant="secondary" size="sm" fullWidth>
                    Sign In
                  </Button>
                </Link>
                <Link href="/signup" className="block">
                  <Button variant="primary" size="sm" fullWidth>
                    Get Started
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
