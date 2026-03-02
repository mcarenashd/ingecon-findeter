"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { DashboardData, CurvaSResponse } from "@/lib/types";
import { EstadoHitoBadge } from "@/components/EstadoBadge";
import { CurvaSChart } from "@/components/CurvaSChart";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [curvaS, setCurvaS] = useState<CurvaSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<DashboardData>("/api/v1/dashboard")
      .then(setData)
      .catch((e) => setError(e.message));
    apiFetch<CurvaSResponse>("/api/v1/dashboard/curva-s")
      .then(setCurvaS)
      .catch(() => {});
  }, []);

  if (error) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Dashboard Ejecutivo</h1>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        Cargando dashboard...
      </div>
    );
  }

  const valorTotal = Number(data.valor_total_obra);
  const valorFormateado = valorTotal >= 1e9
    ? `$${(valorTotal / 1e9).toFixed(1)}B`
    : valorTotal >= 1e6
      ? `$${(valorTotal / 1e6).toFixed(0)}M`
      : `$${valorTotal.toLocaleString("es-CO")}`;

  const avanceGeneral = Number(data.avance_fisico_general).toFixed(1);

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard Ejecutivo</h1>
        <p className="text-sm text-slate-500 mt-1">
          Resumen general de contratos de obra supervisados
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <KPICard
          label="Proyectos de Obra"
          value={String(data.total_contratos_obra)}
          subtitle="Contratos activos"
          color="blue"
        />
        <KPICard
          label="Valor Total Obra"
          value={valorFormateado}
          subtitle="COP — Valor actualizado"
          color="green"
        />
        <KPICard
          label="Hitos en Retraso"
          value={String(data.hitos_en_retraso.length)}
          subtitle={data.hitos_en_retraso.length > 0 ? "Requieren atención" : "Todo al día"}
          color={data.hitos_en_retraso.length > 0 ? "red" : "green"}
        />
        <KPICard
          label="Informes Pendientes"
          value={String(data.total_informes_pendientes)}
          subtitle="Borradores sin radicar"
          color={data.total_informes_pendientes > 0 ? "yellow" : "green"}
        />
      </div>

      {/* Avance general + Hitos retrasados */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Avance general */}
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Avance Físico General
          </h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="flex-1">
              <div className="h-4 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 rounded-full transition-all"
                  style={{ width: `${Math.min(100, Number(avanceGeneral))}%` }}
                />
              </div>
            </div>
            <span className="text-2xl font-bold text-slate-900">{avanceGeneral}%</span>
          </div>
          <div className="mt-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">
              Curva S — Avance Programado vs Ejecutado
              {curvaS && curvaS.datos.length > 0 && (
                <span className="font-normal text-slate-400 ml-2">
                  CTO {curvaS.contrato_numero}
                </span>
              )}
            </h3>
            <CurvaSChart data={curvaS?.datos ?? []} height={200} />
          </div>
        </div>

        {/* Hitos retrasados */}
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Semáforo de Hitos
          </h2>
          {data.hitos_en_retraso.length > 0 ? (
            <div className="overflow-auto max-h-80">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-left px-2 py-2 font-semibold text-slate-600">Contrato</th>
                    <th className="text-left px-2 py-2 font-semibold text-slate-600">Hito</th>
                    <th className="text-center px-2 py-2 font-semibold text-slate-600">Retraso</th>
                    <th className="text-center px-2 py-2 font-semibold text-slate-600">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {data.hitos_en_retraso.map((h) => (
                    <tr key={h.id} className="border-b border-slate-50">
                      <td className="px-2 py-2 text-xs text-slate-500">{h.contrato_numero}</td>
                      <td className="px-2 py-2 max-w-[200px] truncate">{h.descripcion}</td>
                      <td className={`px-2 py-2 text-center font-medium ${h.dias_retraso > 30 ? "text-red-600" : "text-amber-600"}`}>
                        {h.dias_retraso}d
                      </td>
                      <td className="px-2 py-2 text-center">
                        <EstadoHitoBadge estado={h.estado} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center text-slate-400 text-sm">
              Sin hitos en retraso
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function KPICard({
  label,
  value,
  subtitle,
  color,
}: {
  label: string;
  value: string;
  subtitle: string;
  color: "blue" | "green" | "red" | "yellow";
}) {
  const colorMap = {
    blue: "bg-blue-50 border-blue-200 text-blue-700",
    green: "bg-emerald-50 border-emerald-200 text-emerald-700",
    red: "bg-red-50 border-red-200 text-red-700",
    yellow: "bg-amber-50 border-amber-200 text-amber-700",
  };

  return (
    <div className={`rounded-xl border p-5 ${colorMap[color]}`}>
      <p className="text-sm font-medium opacity-80">{label}</p>
      <p className="text-3xl font-bold mt-1">{value}</p>
      <p className="text-xs opacity-60 mt-1">{subtitle}</p>
    </div>
  );
}
