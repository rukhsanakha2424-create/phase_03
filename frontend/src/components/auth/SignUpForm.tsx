"use client";

/**
 * SignUpForm Component
 * Registration form for new user accounts
 */

import { useState } from "react";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { validateSignUpForm } from "@/lib/validation/auth";
import Link from "next/link";

interface SignUpFormProps {
  onSubmit: (email: string, password: string, name?: string) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
  onErrorDismiss?: () => void;
}

export function SignUpForm({
  onSubmit,
  isLoading = false,
  error,
  onErrorDismiss,
}: SignUpFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    const validationError = validateSignUpForm(
      formData.email,
      formData.password,
      formData.name
    );

    if (validationError) {
      setFieldErrors({ [validationError.field]: validationError.message });
      return;
    }

    // Validate password match
    if (formData.password !== formData.confirmPassword) {
      setFieldErrors({ confirmPassword: "Passwords do not match" });
      return;
    }

    try {
      await onSubmit(formData.email, formData.password, formData.name);
    } catch {
      // Error is handled by parent component
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <ErrorAlert
          message={error}
          title="Sign Up Failed"
          onDismiss={onErrorDismiss}
        />
      )}

      <Input
        label="Full Name (Optional)"
        type="text"
        name="name"
        id="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="John Doe"
        disabled={isLoading}
      />

      <Input
        label="Email Address"
        type="email"
        name="email"
        id="email"
        required
        value={formData.email}
        onChange={handleChange}
        placeholder="you@example.com"
        error={fieldErrors.email}
        disabled={isLoading}
      />

      <Input
        label="Password"
        type="password"
        name="password"
        id="password"
        required
        value={formData.password}
        onChange={handleChange}
        placeholder="••••••••"
        helpText="At least 8 characters"
        error={fieldErrors.password}
        disabled={isLoading}
      />

      <Input
        label="Confirm Password"
        type="password"
        name="confirmPassword"
        id="confirmPassword"
        required
        value={formData.confirmPassword}
        onChange={handleChange}
        placeholder="••••••••"
        error={fieldErrors.confirmPassword}
        disabled={isLoading}
      />

      <Button
        type="submit"
        fullWidth
        isLoading={isLoading}
        disabled={isLoading}
      >
        Create Account
      </Button>

      <p className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <Link
          href="/signin"
          className="font-medium text-violet-dark hover:text-violet"
        >
          Sign In
        </Link>
      </p>
    </form>
  );
}
