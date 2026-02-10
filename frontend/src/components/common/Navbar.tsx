// "use client";

// /**
//  * Navbar Component
//  * Modern dashboard navigation bar with user info and sign-out button
//  * Uses consistent gradient logo with landing navbar
//  */

// import { useState } from "react";
// import Link from "next/link";
// import Image from "next/image";
// import { useAuth } from "@/lib/auth/useAuth";
// import { Button } from "./Button";
// import { Menu, X, LogOut, Settings, Bot, BotMessageSquare } from "lucide-react";

// export function Navbar() {
//   const { user, signOut, isLoading } = useAuth();
//   const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

//   const handleSignOut = async () => {
//     try {
//       await signOut();
//     } catch {
//       // Error is handled by auth context
//     }
//   };

//   // Get user initials for avatar
//   const getInitials = (name?: string, email?: string) => {
//     if (name) {
//       return name
//         .split(" ")
//         .map((n) => n[0])
//         .join("")
//         .toUpperCase()
//         .slice(0, 2);
//     }
//     if (email) {
//       return email[0].toUpperCase();
//     }
//     return "U";
//   };

//   const initials = getInitials(user?.name, user?.email);

//   return (
//     <nav className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-gray-200/50">
//       <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
//         <div className="flex h-20 justify-between items-center">
//           {/* Logo */}
//           <Link href="/" className="flex items-center gap-3 ">
//             <Image
//               src="/assets/logo.png"
//               alt="Organify Logo"
//               width={40}
//               height={40}
//               className="w-10 h-10 shadow-md"
//               priority
//             />
//             <span
//               className="text-xl font-bold hidden sm:block"
//               style={{
//                 color: "#323843",
//                 fontFamily: "'Space Grotesk', sans-serif",
//               }}
//             >
//               Organify
//             </span>
//           </Link>

//           {/* Desktop Navigation */}
//           <div className="hidden md:flex md:items-center md:gap-6">
//             {user && (
//               <>
//                 {/* User Info Card */}
//                 <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-gray-50 border border-gray-200">
//                   <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet to-violet-dark flex items-center justify-center shadow-sm">
//                     <span className="text-white text-xs font-bold">
//                       {initials}
//                     </span>
//                   </div>
//                   <div className="flex flex-col gap-0.5 min-w-0">
//                     <p className="text-sm font-semibold text-gray-900 truncate">
//                       {user.name || "User"}
//                     </p>
//                     <p className="text-xs text-gray-500 truncate">
//                       {user.email}
//                     </p>
//                   </div>
//                 </div>

//                 {/* Divider */}
//                 <div className="h-6 w-px bg-gray-200"></div>

//                 {/* Action Buttons */}
//                 <div className="flex items-center gap-2">
//                   <Link href="/profile">
//                     <button
//                       className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-violet transition-colors"
//                       title="Profile settings"
//                     >
//                       <Settings size={20} />
//                     </button>
//                   </Link>

//                   <Button
//                     variant="secondary"
//                     size="sm"
//                     onClick={handleSignOut}
//                     disabled={isLoading}
//                     isLoading={isLoading}
//                     className="flex items-center gap-2"
//                   >
//                     <LogOut size={16} />
//                     Sign Out
//                   </Button>
//                 </div>
//               </>
//             )}
//           </div>

//           {/* Mobile Menu Button */}
//           <button
//             onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
//             className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
//             aria-label="Toggle menu"
//           >
//             {mobileMenuOpen ? (
//               <X size={24} className="text-gray-900" />
//             ) : (
//               <Menu size={24} className="text-gray-900" />
//             )}
//           </button>
//         </div>

//         {/* Mobile Menu */}
//         {mobileMenuOpen && (
//           <div className="md:hidden border-t border-gray-200/50 bg-white/50 backdrop-blur-lg">
//             <div className="px-4 py-6 space-y-4">
//               {user && (
//                 <>
//                   {/* Mobile User Info */}
//                   <div className="flex items-center gap-3 px-3 py-3 rounded-lg bg-gradient-to-r from-violet/10 to-violet-dark/10 border border-violet/20">
//                     <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet to-violet-dark flex items-center justify-center shadow-sm flex-shrink-0">
//                       <span className="text-white text-sm font-bold">
//                         {initials}
//                       </span>
//                     </div>
//                     <div className="flex flex-col gap-0.5 min-w-0">
//                       <p className="text-sm font-semibold text-gray-900">
//                         {user.name || "User"}
//                       </p>
//                       <p className="text-xs text-gray-500 truncate">
//                         {user.email}
//                       </p>
//                     </div>
//                   </div>

//                   {/* Mobile Navigation Links */}
//                   <div className="border-t border-gray-200 pt-4 space-y-2">
//                     <Link href="/profile" className="block">
//                       <button className="w-full px-3 py-2 rounded-lg text-left text-gray-700 hover:bg-violet/10 hover:text-violet font-medium transition-colors text-sm flex items-center gap-2">
//                         <Settings size={16} />
//                         Profile Settings
//                       </button>
//                     </Link>

//                     <Button
//                       variant="danger"
//                       size="sm"
//                       fullWidth
//                       onClick={handleSignOut}
//                       disabled={isLoading}
//                       isLoading={isLoading}
//                       className="flex items-center justify-center gap-2"
//                     >
//                       <LogOut size={16} />
//                       Sign Out
//                     </Button>
//                   </div>
//                 </>
//               )}
//             </div>
//           </div>
//         )}
//       </div>
//     </nav>
//   );
// }





"use client";

/**
 * Navbar Component
 * Modern dashboard navigation bar with user info and sign-out button
 * Uses consistent gradient logo with landing navbar
 */

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/lib/auth/useAuth";
import { Button } from "./Button";
import { Menu, X, LogOut, Settings, Bot, BotMessageSquare } from "lucide-react";
import { AgentIndicator } from "./AgentIndicator";

export function Navbar() {
  const { user, signOut, isLoading } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch {
      // Error is handled by auth context
    }
  };

  const getInitials = (name?: string, email?: string) => {
    if (name) {
      return name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2);
    }
    if (email) {
      return email[0].toUpperCase();
    }
    return "U";
  };

  const initials = getInitials(user?.name, user?.email);

  return (
    <nav className="sticky top-0 z-40 bg-background/80 backdrop-blur-xl border-b border-organify-primary/20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 justify-between items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 ">
            <span
              className="text-xl font-bold hidden sm:block"
              style={{
                color: "#343a40",
                fontFamily: "'Space Grotesk', sans-serif",
              }}
            >
              Organify
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:items-center md:gap-6">
            {user && (
              <>
                {/* Navigation Links */}
                <div className="flex items-center gap-1">
                  <Link href="/tasks">
                    <Button
                      variant="secondary"
                      className="text-slate-light hover:text-organify-primary hover:bg-organify-primary/10"
                    >
                      Tasks
                    </Button>
                  </Link>
                  <Link href="/agents">
                    <Button
                      variant="secondary"
                      className="text-slate-light hover:text-organify-primary hover:bg-organify-primary/10"
                    >
                      Agents
                    </Button>
                  </Link>
                </div>

                {/* Agent Indicator */}
                <AgentIndicator />

                {/* User Info Card */}
                <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-neutral-dark border border-slate-light">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-organify-primary to-organify-secondary flex items-center justify-center shadow-sm">
                    <span className="text-white text-xs font-bold">
                      {initials}
                    </span>
                  </div>
                  <div className="flex flex-col gap-0.5 min-w-0">
                    <p className="text-sm font-semibold text-slate truncate">
                      {user.name || "User"}
                    </p>
                    <p className="text-xs text-slate-light truncate">
                      {user.email}
                    </p>
                  </div>
                </div>

                {/* Divider */}
                <div className="h-6 w-px bg-slate-light"></div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2">
                  <Link href="/profile">
                    <button
                      className="p-2 rounded-lg text-slate-light hover:bg-organify-primary/10 hover:text-organify-primary transition-colors"
                      title="Profile settings"
                    >
                      <Settings size={20} />
                    </button>
                  </Link>

                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={handleSignOut}
                    disabled={isLoading}
                    isLoading={isLoading}
                    className="flex items-center gap-2"
                  >
                    <LogOut size={16} />
                    Sign Out
                  </Button>
                </div>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-organify-primary/10 transition-colors"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X size={24} className="text-organify-primary" />
            ) : (
              <Menu size={24} className="text-organify-primary" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-organify-primary/20 bg-background/50 backdrop-blur-lg">
            <div className="px-4 py-6 space-y-4">
              {/* Mobile Logo */}
              <div className="flex items-center gap-3 mb-4">
                <span
                  className="text-xl font-bold"
                  style={{
                    color: "#343a40",
                    fontFamily: "'Space Grotesk', sans-serif",
                  }}
                >
                  Organify
                </span>
              </div>

              {user && (
                <>
                  {/* Agent Indicator */}
                <div className="px-3 py-2">
                  <AgentIndicator />
                </div>

                {/* Mobile User Info */}
                  <div className="flex items-center gap-3 px-3 py-3 rounded-lg bg-gradient-to-r from-organify-primary/10 to-organify-secondary/10 border border-organify-primary/20">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-organify-primary to-organify-secondary flex items-center justify-center shadow-sm flex-shrink-0">
                      <span className="text-white text-sm font-bold">
                        {initials}
                      </span>
                    </div>
                    <div className="flex flex-col gap-0.5 min-w-0">
                      <p className="text-sm font-semibold text-slate">
                        {user.name || "User"}
                      </p>
                      <p className="text-xs text-slate-light truncate">
                        {user.email}
                      </p>
                    </div>
                  </div>

                  {/* Mobile Navigation Links */}
                  <div className="border-t border-organify-primary/20 pt-4 space-y-2">
                    <Link href="/tasks" className="block">
                      <button className="w-full px-3 py-2 rounded-lg text-left text-slate hover:bg-organify-primary/10 hover:text-organify-primary font-medium transition-colors text-sm flex items-center gap-2">
                        <BotMessageSquare size={16} />
                        Tasks
                      </button>
                    </Link>
                    
                    <Link href="/agents" className="block">
                      <button className="w-full px-3 py-2 rounded-lg text-left text-slate hover:bg-organify-primary/10 hover:text-organify-primary font-medium transition-colors text-sm flex items-center gap-2">
                        <Bot size={16} />
                        Agents
                      </button>
                    </Link>

                    <Link href="/profile" className="block">
                      <button className="w-full px-3 py-2 rounded-lg text-left text-slate hover:bg-organify-primary/10 hover:text-organify-primary font-medium transition-colors text-sm flex items-center gap-2">
                        <Settings size={16} />
                        Profile Settings
                      </button>
                    </Link>

                    <Button
                      variant="danger"
                      size="sm"
                      fullWidth
                      onClick={handleSignOut}
                      disabled={isLoading}
                      isLoading={isLoading}
                      className="flex items-center justify-center gap-2"
                    >
                      <LogOut size={16} />
                      Sign Out
                    </Button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
