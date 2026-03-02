"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import type { ContratoObra } from "@/lib/types";

export default function ContratosPage() {
  const [contratos, setContratos] = useState<ContratoObra[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch<ContratoObra[]>("/api/v1/contratos/obra")
      .then(setContratos)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (error) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">
          Gestión de Contratos de Obra
        </h1>
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        Cargando contratos...
      </div>
    );
  }

  function fmtValor(valor: string): string {
    const n = Number(valor);
    if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
    if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`;
    return `$${n.toLocaleString("es-CO")}`;
  }

  function fmtFecha(iso: string): string {
    return new Date(iso + "T00:00:00").toLocaleDateString("es-CO", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  }

  function diasRestantes(fechaFin: string): { texto: string; color: string } {
    const hoy = new Date();
    const fin = new Date(fechaFin + "T00:00:00");
    const diff = Math.ceil((fin.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
    if (diff < 0) return { texto: `${Math.abs(diff)}d vencido`, color: "text-red-600" };
    if (diff < 30) return { texto: `${diff}d restantes`, color: "text-amber-600" };
    return { texto: `${diff}d restantes`, color: "text-slate-500" };
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">
          Gestión de Contratos de Obra
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          {contratos.length} contrato{contratos.length !== 1 ? "s" : ""} de obra
          supervisado{contratos.length !== 1 ? "s" : ""}
        </p>
      </div>

      {contratos.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400">
          No hay contratos de obra registrados.
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="text-left px-4 py-3 font-semibold text-slate-700">
                  Contrato / Objeto
                </th>
                <th className="text-left px-4 py-3 font-semibold text-slate-700">
                  Contratista
                </th>
                <th className="text-right px-4 py-3 font-semibold text-slate-700">
                  Valor Actualizado
                </th>
                <th className="text-center px-4 py-3 font-semibold text-slate-700">
                  Plazo
                </th>
                <th className="text-center px-4 py-3 font-semibold text-slate-700">
                  Periodo
                </th>
                <th className="text-center px-4 py-3 font-semibold text-slate-700">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody>
              {contratos.map((c) => {
                const plazo = diasRestantes(c.fecha_terminacion);
                return (
                  <tr
                    key={c.id}
                    className="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td className="px-4 py-3">
                      <div className="font-medium text-slate-900">
                        CTO {c.numero}
                      </div>
                      <div className="text-xs text-slate-400 mt-0.5 max-w-md truncate">
                        {c.objeto}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-slate-600">{c.contratista}</td>
                    <td className="px-4 py-3 text-right font-mono text-slate-700">
                      {fmtValor(c.valor_actualizado)}
                      {Number(c.adiciones) > 0 && (
                        <div className="text-xs text-slate-400">
                          +{fmtValor(c.adiciones)} adiciones
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div className="text-slate-700">{c.plazo_dias} días</div>
                      <div className={`text-xs ${plazo.color}`}>{plazo.texto}</div>
                    </td>
                    <td className="px-4 py-3 text-center text-xs text-slate-500">
                      <div>{fmtFecha(c.fecha_inicio)}</div>
                      <div className="text-slate-400">a</div>
                      <div>{fmtFecha(c.fecha_terminacion)}</div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <Link
                        href={`/contratos/${c.id}`}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        Ver detalle
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
