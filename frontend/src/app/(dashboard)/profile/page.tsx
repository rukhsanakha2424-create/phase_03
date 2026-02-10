"use client";

/**
 * Profile Page
 * User profile and sign-out
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/useAuth";
import { Button } from "@/components/common/Button";
import { Container } from "@/components/layout/Container";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ArrowLeftToLine } from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, signOut, isLoading } = useAuth();
  const [isSigningOut, setIsSigningOut] = useState(false);

  if (!isAuthenticated || !user) {
    return null; // Middleware should redirect to signin
  }

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await signOut();
      // Redirect is handled by auth context
    } catch {
      setIsSigningOut(false);
    }
  };

  if (isLoading || isSigningOut) {
    return <LoadingSpinner message="Signing out..." fullscreen />;
  }

  return (
    <Container size="sm" className="py-8">
      <div className="space-y-8">
        {/* Profile Header */}
        <div>
          <h1
            className="text-3xl font-semibold"
            style={{
              color: "#323843",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            Profile
          </h1>
          <p className="mt-2 text-gray-600">Manage your account</p>
        </div>

        {/* Profile Information */}
        <div className="rounded-lg bg-white p-8 shadow-sm border border-gray-200 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <p className="mt-1 text-lg text-gray-900">
              {user.name || "Not set"}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Email Address
            </label>
            <p className="mt-1 text-lg text-gray-900">{user.email}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              User ID
            </label>
            <p className="mt-1 font-mono text-sm text-gray-600">{user.id}</p>
          </div>

          {user.createdAt && (
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Member Since
              </label>
              <p className="mt-1 text-lg text-gray-900">
                {new Date(user.createdAt).toLocaleDateString()}
              </p>
            </div>
          )}

          {/* Sign Out Section */}
          <div className="border-t border-gray-200 pt-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Session
            </h2>
            <Button
              variant="danger"
              onClick={handleSignOut}
              disabled={isLoading}
              isLoading={isSigningOut}
            >
              Sign Out
            </Button>
            <p className="mt-2 text-sm text-gray-600">
              This will end your current session and redirect you to the sign-in
              page.
            </p>
          </div>
        </div>

        {/* Back to Tasks */}
        <Button variant="secondary" onClick={() => router.push("/tasks")}>
          <ArrowLeftToLine />
          <span>Back to Tasks</span>
        </Button>
      </div>
    </Container>
  );
}
