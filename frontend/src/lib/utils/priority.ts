/**
 * Priority utility functions
 * Provides color, icon, and label mappings for task priorities
 */

import {
  Minus,
  LucideIcon,
  ChevronUp,
  ChevronsDown,
  ChevronDown,
} from "lucide-react";

export type PriorityLevel = "low" | "medium" | "high";

export function getPriorityColor(priority?: string): string {
  switch (priority?.toLowerCase()) {
    case "high":
      return "oklch(70.4% 0.191 22.216)"; // Red
    case "medium":
      return "oklch(82.8% 0.189 84.429)"; // Yellow
    case "low":
      return "oklch(76.5% 0.177 163.223)"; // Green
    default:
      return "oklch(82.8% 0.189 84.429)"; // Default to medium (yellow)
  }
}

export function getPriorityLabel(priority?: string): string {
  switch (priority?.toLowerCase()) {
    case "high":
      return "High";
    case "medium":
      return "Medium";
    case "low":
      return "Low";
    default:
      return "Medium";
  }
}

export function getPriorityIcon(priority?: string): LucideIcon {
  switch (priority?.toLowerCase()) {
    case "high":
      return ChevronUp;
    case "medium":
      return ChevronDown;
    case "low":
      return ChevronsDown;
    default:
      return Minus;
  }
}

export function getPriorityOrder(priority?: string): number {
  switch (priority?.toLowerCase()) {
    case "high":
      return 3;
    case "medium":
      return 2;
    case "low":
      return 1;
    default:
      return 2;
  }
}

export const PRIORITY_OPTIONS: Array<{ value: string; label: string }> = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
];
