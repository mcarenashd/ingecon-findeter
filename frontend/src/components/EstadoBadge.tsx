import type { EstadoInforme, EstadoPlanAccion, EstadoHito } from "@/lib/types";

const ESTADO_INFORME_CONFIG: Record<
  EstadoInforme,
  { label: string; bg: string; text: string }
> = {
  borrador: { label: "Borrador", bg: "bg-slate-100", text: "text-slate-700" },
  en_revision: { label: "En Revisión", bg: "bg-blue-100", text: "text-blue-700" },
  aprobado: { label: "Aprobado", bg: "bg-emerald-100", text: "text-emerald-700" },
  radicado: { label: "Radicado", bg: "bg-purple-100", text: "text-purple-700" },
};

const ESTADO_PLAN_CONFIG: Record<
  EstadoPlanAccion,
  { label: string; bg: string; text: string }
> = {
  pendiente: { label: "Pendiente", bg: "bg-slate-100", text: "text-slate-600" },
  en_proceso: { label: "En Proceso", bg: "bg-blue-100", text: "text-blue-700" },
  cumplido: { label: "Cumplido", bg: "bg-emerald-100", text: "text-emerald-700" },
  vencido: { label: "Vencido", bg: "bg-red-100", text: "text-red-700" },
};

const ESTADO_HITO_CONFIG: Record<
  EstadoHito,
  { label: string; bg: string; text: string }
> = {
  no_iniciado: { label: "No Iniciado", bg: "bg-slate-100", text: "text-slate-600" },
  en_proceso: { label: "En Proceso", bg: "bg-blue-100", text: "text-blue-700" },
  cumplido: { label: "Cumplido", bg: "bg-emerald-100", text: "text-emerald-700" },
  vencido: { label: "Vencido", bg: "bg-red-100", text: "text-red-700" },
};

export function EstadoInformeBadge({ estado }: { estado: EstadoInforme }) {
  const config = ESTADO_INFORME_CONFIG[estado];
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
}

export function EstadoPlanBadge({ estado }: { estado: EstadoPlanAccion }) {
  const config = ESTADO_PLAN_CONFIG[estado];
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
}

export function EstadoHitoBadge({ estado }: { estado: EstadoHito }) {
  const config = ESTADO_HITO_CONFIG[estado];
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
}
