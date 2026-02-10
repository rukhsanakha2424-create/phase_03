"use client";

/**
 * SignInForm Component
 * Login form for existing users
 */

import { useState } from "react";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { validateSignInForm } from "@/lib/validation/auth";
import Link from "next/link";

interface SignInFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
  onErrorDismiss?: () => void;
}

export function SignInForm({
  onSubmit,
  isLoading = false,
  error,
  onErrorDismiss,
}: SignInFormProps) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
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
    const validationError = validateSignInForm(
      formData.email,
      formData.password
    );

    if (validationError) {
      setFieldErrors({ [validationError.field]: validationError.message });
      return;
    }

    try {
      await onSubmit(formData.email, formData.password);
    } catch {
      // Error is handled by parent component
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <ErrorAlert
          message={error}
          title="Sign In Failed"
          onDismiss={onErrorDismiss}
        />
      )}

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
        error={fieldErrors.password}
        disabled={isLoading}
      />

      <Button
        type="submit"
        fullWidth
        isLoading={isLoading}
        disabled={isLoading}
      >
        Sign In
      </Button>

      <p className="text-center text-sm text-gray-600">
        Don&apos;t have an account?{" "}
        <Link
          href="/signup"
          className="font-medium text-violet-dark hover:text-violet"
        >
          Sign Up
        </Link>
      </p>
    </form>
  );
}
