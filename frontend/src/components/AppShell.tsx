"use client";

import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";
import Sidebar from "@/components/Sidebar";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const { token, isLoading } = useAuth();
  const pathname = usePathname();

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="text-slate-400 text-sm">Cargando...</div>
      </div>
    );
  }

  // Login page — no sidebar
  if (pathname === "/login") {
    return <>{children}</>;
  }

  // Not authenticated — the auth provider will redirect
  if (!token) {
    return null;
  }

  // Authenticated — show sidebar + content
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6 overflow-auto">{children}</main>
    </div>
  );
}
