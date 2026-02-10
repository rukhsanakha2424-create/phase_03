import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "'Roboto', var(--font-roboto)",
          "system-ui",
          "sans-serif",
        ],
        grotesk: [
          "'Space Grotesk', var(--font-space-grotesk)",
          "system-ui",
          "sans-serif",
        ],
      },
      colors: {
        // Organify Brand Colors
        organify: {
          primary: {
            DEFAULT: "#4361ee", // Professional Blue
            light: "#4895ef",
            dark: "#3a56d4",
          },
          secondary: {
            DEFAULT: "#3f37c9", // Deep Purple-Blue
            light: "#560bad",
            dark: "#2d28a9",
          },
          accent: {
            DEFAULT: "#4cc9f0", // Modern Cyan
            light: "#72e0f2",
            dark: "#3da8d6",
          },
          neutral: {
            DEFAULT: "#f8f9fa", // Clean Background
            light: "#ffffff",
            dark: "#e9ecef",
          },
        },
        // Productivity-focused colors
        slate: {
          DEFAULT: "#343a40", // Professional Gray
          light: "#6c757d",
          dark: "#212529",
        },
        // Semantic colors
        error: "#e63946",
        errorLight: "#ff7e8b",
        warning: "#fca311",
        success: "#2a9d8f",
        background: "#f0f2f5", // Clean workspace background
      },
      spacing: {
        "128": "32rem",
        // Design system spacing scale (4px base grid)
        xs: "4px",
        sm: "8px",
        md: "12px",
        lg: "24px",
        xl: "32px",
        "2xl": "48px",
      },
      screens: {
        mobile: "320px",
        tablet: "768px",
        desktop: "1024px",
      },
      borderRadius: {
        none: "0",
        sm: "4px",
        base: "8px",
        md: "12px",
        lg: "16px",
        full: "9999px",
      },
      boxShadow: {
        sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        base: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
        md: "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
        lg: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
        xl: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
      },
      transitionDuration: {
        fast: "150ms",
        base: "200ms",
        slow: "300ms",
        slowest: "500ms",
      },
      keyframes: {
        "jello-vertical": {
          "0%": { transform: "scale3d(1, 1, 1)" },
          "30%": { transform: "scale3d(0.75, 1.25, 1)" },
          "40%": { transform: "scale3d(1.25, 0.75, 1)" },
          "50%": { transform: "scale3d(0.85, 1.15, 1)" },
          "65%": { transform: "scale3d(1.05, 0.95, 1)" },
          "75%": { transform: "scale3d(0.95, 1.05, 1)" },
          "100%": { transform: "scale3d(1, 1, 1)" },
        },
      },
      animation: {
        "jello-vertical": "jello-vertical 0.9s both",
      },
    },
  },
  plugins: [],
};

export default config;
