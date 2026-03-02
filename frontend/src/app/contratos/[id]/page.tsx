"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import type { ContratoObra, Hito, CurvaSResponse } from "@/lib/types";
import { EstadoHitoBadge } from "@/components/EstadoBadge";
import { CurvaSChart } from "@/components/CurvaSChart";

export default function ContratoDetallePage() {
  const params = useParams();
  const id = params.id as string;

  const [contrato, setContrato] = useState<ContratoObra | null>(null);
  const [hitos, setHitos] = useState<Hito[]>([]);
  const [curvaS, setCurvaS] = useState<CurvaSResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiFetch<ContratoObra>(`/api/v1/contratos/obra/${id}`),
      apiFetch<Hito[]>(`/api/v1/contratos/obra/${id}/hitos`),
    ])
      .then(([c, h]) => {
        setContrato(c);
        setHitos(h);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
    apiFetch<CurvaSResponse>(`/api/v1/informes/semanales/curva-s/${id}`)
      .then(setCurvaS)
      .catch(() => {});
  }, [id]);

  if (error) {
    return (
      <div>
        <Link
          href="/contratos"
          className="text-sm text-blue-600 hover:text-blue-800 mb-4 inline-block"
        >
          &larr; Volver a contratos
        </Link>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (loading || !contrato) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        Cargando contrato...
      </div>
    );
  }

  function fmtValor(valor: string): string {
    return `$${Number(valor).toLocaleString("es-CO")}`;
  }

  function fmtFecha(iso: string): string {
    return new Date(iso + "T00:00:00").toLocaleDateString("es-CO", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  }

  const hitosCumplidos = hitos.filter((h) => h.estado === "cumplido").length;
  const hitosVencidos = hitos.filter((h) => h.estado === "vencido").length;
  const avancePromedio =
    hitos.length > 0
      ? (
          hitos.reduce((acc, h) => acc + Number(h.avance_porcentaje), 0) /
          hitos.length
        ).toFixed(1)
      : "0.0";

  return (
    <div>
      {/* Breadcrumb */}
      <Link
        href="/contratos"
        className="text-sm text-blue-600 hover:text-blue-800 mb-4 inline-block"
      >
        &larr; Volver a contratos
      </Link>

      {/* Contract header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              CTO {contrato.numero}
            </h1>
            <p className="text-sm text-slate-500 mt-1 max-w-2xl">
              {contrato.objeto}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <InfoItem label="Contratista" value={contrato.contratista} />
          <InfoItem label="Valor Actualizado" value={fmtValor(contrato.valor_actualizado)} />
          <InfoItem label="Plazo" value={`${contrato.plazo_dias} días`} />
          <InfoItem
            label="Periodo"
            value={`${fmtFecha(contrato.fecha_inicio)} — ${fmtFecha(contrato.fecha_terminacion)}`}
          />
          {Number(contrato.adiciones) > 0 && (
            <InfoItem label="Adiciones" value={fmtValor(contrato.adiciones)} />
          )}
          <InfoItem label="Valor Inicial" value={fmtValor(contrato.valor_inicial)} />
        </div>
      </div>

      {/* KPI mini cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <MiniKPI label="Total Hitos" value={String(hitos.length)} color="blue" />
        <MiniKPI label="Cumplidos" value={String(hitosCumplidos)} color="green" />
        <MiniKPI
          label="Vencidos"
          value={String(hitosVencidos)}
          color={hitosVencidos > 0 ? "red" : "green"}
        />
        <MiniKPI label="Avance Promedio" value={`${avancePromedio}%`} color="blue" />
      </div>

      {/* Hitos table */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">
          Hitos del Contrato
        </h2>

        {hitos.length === 0 ? (
          <div className="h-32 flex items-center justify-center text-slate-400 text-sm">
            No hay hitos registrados para este contrato.
          </div>
        ) : (
          <div className="overflow-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="text-center px-3 py-2 font-semibold text-slate-600 w-12">
                    #
                  </th>
                  <th className="text-left px-3 py-2 font-semibold text-slate-600">
                    Descripción
                  </th>
                  <th className="text-center px-3 py-2 font-semibold text-slate-600">
                    Fecha Programada
                  </th>
                  <th className="text-center px-3 py-2 font-semibold text-slate-600">
                    Fecha Real
                  </th>
                  <th className="text-center px-3 py-2 font-semibold text-slate-600">
                    Avance
                  </th>
                  <th className="text-center px-3 py-2 font-semibold text-slate-600">
                    Estado
                  </th>
                </tr>
              </thead>
              <tbody>
                {hitos.map((h) => (
                  <tr key={h.id} className="border-b border-slate-50">
                    <td className="px-3 py-2 text-center text-slate-500 font-mono">
                      {h.numero}
                    </td>
                    <td className="px-3 py-2 text-slate-700">{h.descripcion}</td>
                    <td className="px-3 py-2 text-center text-xs text-slate-500">
                      {fmtFecha(h.fecha_programada)}
                    </td>
                    <td className="px-3 py-2 text-center text-xs text-slate-500">
                      {h.fecha_real ? fmtFecha(h.fecha_real) : "—"}
                    </td>
                    <td className="px-3 py-2 text-center">
                      <div className="flex items-center gap-2 justify-center">
                        <div className="w-16 h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              Number(h.avance_porcentaje) >= 100
                                ? "bg-emerald-500"
                                : Number(h.avance_porcentaje) > 50
                                  ? "bg-blue-500"
                                  : "bg-amber-500"
                            }`}
                            style={{
                              width: `${Math.min(100, Number(h.avance_porcentaje))}%`,
                            }}
                          />
                        </div>
                        <span className="text-xs font-medium text-slate-600 w-10 text-right">
                          {Number(h.avance_porcentaje).toFixed(0)}%
                        </span>
                      </div>
                    </td>
                    <td className="px-3 py-2 text-center">
                      <EstadoHitoBadge estado={h.estado} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Curva S */}
      {curvaS && curvaS.datos.length >= 2 && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 mt-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Curva S — Avance Programado vs Ejecutado
          </h2>
          <CurvaSChart data={curvaS.datos} height={300} />
        </div>
      )}
    </div>
  );
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm text-slate-700 mt-0.5">{value}</p>
    </div>
  );
}

function MiniKPI({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: "blue" | "green" | "red";
}) {
  const colorMap = {
    blue: "bg-blue-50 border-blue-200 text-blue-700",
    green: "bg-emerald-50 border-emerald-200 text-emerald-700",
    red: "bg-red-50 border-red-200 text-red-700",
  };

  return (
    <div className={`rounded-xl border p-4 ${colorMap[color]}`}>
      <p className="text-xs font-medium opacity-80">{label}</p>
      <p className="text-2xl font-bold mt-0.5">{value}</p>
    </div>
  );
}
