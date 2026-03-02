import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth";
import AppShell from "@/components/AppShell";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ingecon Findeter - Seguimiento de Interventoría",
  description:
    "Aplicación de seguimiento de interventoría para Consorcio Infraestructura Bosa",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased">
        <AuthProvider>
          <AppShell>{children}</AppShell>
        </AuthProvider>
      </body>
    </html>
  );
}
