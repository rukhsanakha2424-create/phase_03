import React from "react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <div className="mb-8 text-center">
          <h1
            className="text-2xl font-bold "
            style={{
              color: "#323843",
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            Organify
          </h1>
          <p className="text-gray-600 text-sm mt-2">
            Manage your tasks efficiently
          </p>
        </div>
        z{children}
      </div>
    </div>
  );
}
