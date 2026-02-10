/**
 * Auth Layout
 * Layout for authentication pages (signup, signin)
 * No navbar - centered form layout
 */

import { ReactNode } from "react";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-4 py-12">
      <div className="w-full max-w-md space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1
            className="text-5xl font-bold "
            style={{
              color: "#323843",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            Organify
          </h1>
          <p className="mt-2 text-gray-600">Manage your tasks with ease</p>
        </div>

        {/* Form Container */}
        <div className="rounded-lg bg-[#ffff] p-8 shadow-md">{children}</div>
      </div>
    </div>
  );
}
