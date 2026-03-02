const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getAuthHeaders(): Record<string, string> {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
      ...options?.headers,
    },
  });
  if (!res.ok) {
    if (res.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
      throw new Error("Sesión expirada");
    }
    const error = await res.json().catch(() => ({ detail: "Error de conexión" }));
    throw new Error(error.detail || `Error ${res.status}`);
  }
  return res.json();
}

export async function apiUpload<T>(path: string, formData: FormData): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { ...getAuthHeaders() },
    body: formData,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Error de conexión" }));
    throw new Error(error.detail || `Error ${res.status}`);
  }
  return res.json();
}

export async function apiDownload(path: string): Promise<Blob> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: { ...getAuthHeaders() },
  });
  if (!res.ok) {
    throw new Error(`Error ${res.status}`);
  }
  return res.blob();
}

export function fotoUrl(fotoId: number): string {
  return `${API_BASE}/api/v1/fotos/${fotoId}/archivo`;
}
