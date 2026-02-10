
"use client";

/**
 * Auth Context and Provider
 * Manages global authentication state
 * Provides sign-up, sign-in, sign-out functions
 */

import React, { createContext, useState, useCallback, useEffect, ReactNode } from "react";
import { clearToken, saveToken, getUser } from "@/lib/auth/jwt-storage";
import { User, AuthError } from "@/lib/api/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: AuthError | null;
  signUp: (email: string, password: string, name?: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  clearError: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<AuthError | null>(null);

  // Restore user from localStorage on mount
  useEffect(() => {
    try {
      const savedUser = getUser();
      if (savedUser) {
        setUser(savedUser);
      }
    } catch (err) {
      console.error("Failed to restore user from localStorage:", err);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // MOCK SIGNUP - Replace this when you have real backend auth
  const signUp = useCallback(
    async (email: string, password: string, name?: string) => {
      setIsLoading(true);
      setError(null);

      try {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockUser = {
          id: Math.random().toString(36).substr(2, 9),
          email,
          name: name || email.split('@')[0],
        };
        
        const mockToken = 'mock-jwt-token-' + Date.now();
        
        setUser(mockUser);
        saveToken(mockToken, mockUser);

        // Redirect to tasks page
        if (typeof window !== "undefined") {
          window.location.href = "/tasks";
        }
      } catch (err) {
        const authError = err as AuthError;
        setError(authError);
        throw authError;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  // MOCK SIGNIN - Replace this when you have real backend auth
  const signIn = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockUser = {
        id: Math.random().toString(36).substr(2, 9),
        email,
        name: email.split('@')[0],
      };
      
      const mockToken = 'mock-jwt-token-' + Date.now();
      
      setUser(mockUser);
      saveToken(mockToken, mockUser);

      // Redirect to tasks page
      if (typeof window !== "undefined") {
        window.location.href = "/tasks";
      }
    } catch (err) {
      const authError = err as AuthError;
      setError(authError);
      throw authError;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const signOut = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      clearToken();
      setUser(null);

      if (typeof window !== "undefined") {
        window.location.href = "/signin";
      }
    } catch (err) {
      const authError = err as AuthError;
      setError(authError);
      throw authError;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    error,
    signUp,
    signIn,
    signOut,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}




/**
 * Auth Context and Provider
 * Manages global authentication state
 * Provides sign-up, sign-in, sign-out functions
 */

// import React, { createContext, useState, useCallback, useEffect, ReactNode } from "react";
// import { clearToken, saveToken, getUser } from "@/lib/auth/jwt-storage";
// import { User, AuthError } from "@/lib/api/types";

// const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// export interface AuthContextType {
//   user: User | null;
//   isAuthenticated: boolean;
//   isLoading: boolean;
//   error: AuthError | null;
//   signUp: (email: string, password: string, name?: string) => Promise<void>;
//   signIn: (email: string, password: string) => Promise<void>;
//   signOut: () => Promise<void>;
//   clearError: () => void;
// }

// export const AuthContext = createContext<AuthContextType | undefined>(
//   undefined
// );

// export interface AuthProviderProps {
//   children: ReactNode;
// }

// export function AuthProvider({ children }: AuthProviderProps) {
//   const [user, setUser] = useState<User | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState<AuthError | null>(null);

//   // Restore user from localStorage on mount
//   useEffect(() => {
//     try {
//       const savedUser = getUser();
//       if (savedUser) {
//         setUser(savedUser);
//       }
//     } catch (err) {
//       // If there's an error restoring user, just continue
//       console.error("Failed to restore user from localStorage:", err);
//     }
//   }, []);

//   const clearError = useCallback(() => {
//     setError(null);
//   }, []);

//   const signUp = useCallback(
//     async (email: string, password: string, name?: string) => {
//       setIsLoading(true);
//       setError(null);

//       try {
//         const response = await fetch(`${API_BASE_URL}/auth/signup`, {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ email, password, name }),
//         });

//         if (!response.ok) {
//           const data = await response.json();
//           throw {
//             code: "SIGNUP_FAILED",
//             message: data.detail || "Sign-up failed",
//           };
//         }

//         const data = await response.json();
//         setUser(data.user);

//         // Save token to localStorage
//         saveToken(data.token, data.user);

//         // Redirect to tasks page
//         if (typeof window !== "undefined") {
//           window.location.href = "/tasks";
//         }
//       } catch (err) {
//         const authError = err as AuthError;
//         setError(authError);
//         throw authError;
//       } finally {
//         setIsLoading(false);
//       }
//     },
//     []
//   );

//   const signIn = useCallback(async (email: string, password: string) => {
//     setIsLoading(true);
//     setError(null);

//     try {
//       const response = await fetch(`${API_BASE_URL}/auth/signin`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ email, password }),
//       });

//       if (!response.ok) {
//         const data = await response.json();
//         throw {
//           code: "SIGNIN_FAILED",
//           message: data.detail || "Sign-in failed",
//         };
//       }

//       const data = await response.json();
//       setUser(data.user);

//       // Save token to localStorage
//       saveToken(data.token, data.user);

//       // Redirect to tasks page
//       if (typeof window !== "undefined") {
//         window.location.href = "/tasks";
//       }
//     } catch (err) {
//       const authError = err as AuthError;
//       setError(authError);
//       throw authError;
//     } finally {
//       setIsLoading(false);
//     }
//   }, []);

//   const signOut = useCallback(async () => {
//     setIsLoading(true);
//     setError(null);

//     try {
//       // Clear JWT token from localStorage
//       clearToken();
//       setUser(null);

//       // Redirect to signin page
//       if (typeof window !== "undefined") {
//         window.location.href = "/signin";
//       }
//     } catch (err) {
//       const authError = err as AuthError;
//       setError(authError);
//       throw authError;
//     } finally {
//       setIsLoading(false);
//     }
//   }, []);

//   const value: AuthContextType = {
//     user,
//     isAuthenticated: !!user,
//     isLoading,
//     error,
//     signUp,
//     signIn,
//     signOut,
//     clearError,
//   };

//   return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
// }




