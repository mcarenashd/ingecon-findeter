"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useRouter, usePathname } from "next/navigation";

interface User {
  email: string;
  role: string;
  nombre: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: async () => {},
  logout: () => {},
  isLoading: true,
});

export function useAuth() {
  return useContext(AuthContext);
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function parseJwt(token: string): { sub: string; role: string; exp: number } | null {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

const ROLE_LABELS: Record<string, string> = {
  director_interventoria: "Director de Interventoría",
  residente_tecnico: "Residente Técnico",
  residente_sst: "Residente SST",
  residente_ambiental: "Residente Ambiental",
  residente_social: "Residente Social",
  residente_administrativo: "Residente Administrativo",
  supervisor: "Supervisor",
};

export function rolLabel(role: string): string {
  return ROLE_LABELS[role] || role;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Restore session from localStorage on mount
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");
    if (savedToken && savedUser) {
      const payload = parseJwt(savedToken);
      if (payload && payload.exp * 1000 > Date.now()) {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } else {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
    }
    setIsLoading(false);
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (isLoading) return;
    if (!token && pathname !== "/login") {
      router.replace("/login");
    }
  }, [token, pathname, isLoading, router]);

  const login = useCallback(async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Error de conexión" }));
      throw new Error(err.detail || "Credenciales incorrectas");
    }

    const data = await res.json();
    const accessToken = data.access_token;
    const payload = parseJwt(accessToken);

    if (!payload) throw new Error("Token inválido");

    const newUser: User = {
      email: payload.sub,
      role: payload.role,
      nombre: payload.sub.split("@")[0],
    };

    setToken(accessToken);
    setUser(newUser);
    localStorage.setItem("token", accessToken);
    localStorage.setItem("user", JSON.stringify(newUser));

    router.replace("/dashboard");
  }, [router]);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    router.replace("/login");
  }, [router]);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}
