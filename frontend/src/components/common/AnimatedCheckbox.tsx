"use client";

import React from "react";
import { Check, CheckCircle2, Circle, Minus } from "lucide-react";
import styles from "./AnimatedCheckbox.module.css";

interface AnimatedCheckboxProps {
  id: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
  ariaLabel?: string;
}

/**
 * AnimatedCheckbox Component
 *
 * A beautiful animated checkbox with smooth transitions and firework effect.
 * Features:
 * - Custom animated checkmark with dual-line animation
 * - Strikethrough effect on checked state
 * - Firework particle animation
 * - Smooth label transitions
 * - Fully accessible with ARIA labels
 *
 * @example
 * const [isChecked, setIsChecked] = useState(false)
 * <AnimatedCheckbox
 *   id="task-1"
 *   checked={isChecked}
 *   onChange={setIsChecked}
 *   label="Complete this task"
 * />
 */
export function AnimatedCheckbox({
  id,
  checked,
  onChange,
  label,
  disabled = false,
  ariaLabel,
}: AnimatedCheckboxProps) {
  return (
    <div className={styles.wrapper}>
      <input
        id={id}
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        disabled={disabled}
        className={styles.checkbox}
        aria-label={ariaLabel || label || "Checkbox"}
        aria-checked={checked}
      />
      <label htmlFor={id} className={styles.label}>
        <div className="flex items-center gap-2">
          {checked ? (
            <Check
              size={20}
              className="text-slate-dark flex-shrink-0 transition-colors"
              strokeWidth={2.5}
            />
          ) : (
            <Minus
              size={20}
              className="text-slate-dark flex-shrink-0 transition-colors"
              strokeWidth={2}
            />
          )}
          {label && <span>{label}</span>}
        </div>
      </label>
    </div>
  );
}
