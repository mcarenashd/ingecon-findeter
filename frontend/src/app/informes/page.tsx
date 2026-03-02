"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import type { InformeSemanalList, ContratoObra, EstadoInforme } from "@/lib/types";
import { EstadoInformeBadge } from "@/components/EstadoBadge";

export default function InformesPage() {
  const [informes, setInformes] = useState<InformeSemanalList[]>([]);
  const [contratos, setContratos] = useState<ContratoObra[]>([]);
  const [contratoId, setContratoId] = useState<number | null>(null);
  const [filtroEstado, setFiltroEstado] = useState<EstadoInforme | "">("");
  const [loading, setLoading] = useState(true);
  const [generando, setGenerando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Cargar contratos
  useEffect(() => {
    apiFetch<ContratoObra[]>("/api/v1/contratos/obra")
      .then((data) => {
        setContratos(data);
        if (data.length > 0 && !contratoId) {
          setContratoId(data[0].id);
        }
      })
      .catch(() => setError("Error cargando contratos"));
  }, []);

  // Cargar informes cuando cambia el contrato o filtro
  useEffect(() => {
    if (!contratoId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    let url = `/api/v1/informes/semanales?contrato_obra_id=${contratoId}`;
    if (filtroEstado) url += `&estado=${filtroEstado}`;
    apiFetch<InformeSemanalList[]>(url)
      .then(setInformes)
      .catch(() => setError("Error cargando informes"))
      .finally(() => setLoading(false));
  }, [contratoId, filtroEstado]);

  const handleGenerar = async () => {
    if (!contratoId) return;
    setGenerando(true);
    setError(null);

    // Calcular semana actual (lunes a domingo)
    const today = new Date();
    const dayOfWeek = today.getDay();
    const monday = new Date(today);
    monday.setDate(today.getDate() - ((dayOfWeek + 6) % 7));
    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);

    const fmt = (d: Date) => d.toISOString().split("T")[0];

    try {
      await apiFetch<InformeSemanalList>("/api/v1/informes/semanales/generar", {
        method: "POST",
        body: JSON.stringify({
          contrato_obra_id: contratoId,
          semana_inicio: fmt(monday),
          semana_fin: fmt(sunday),
        }),
      });
      // Recargar lista
      const url = `/api/v1/informes/semanales?contrato_obra_id=${contratoId}`;
      const data = await apiFetch<InformeSemanalList[]>(url);
      setInformes(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error generando informe");
    } finally {
      setGenerando(false);
    }
  };

  const estados: { value: EstadoInforme | ""; label: string }[] = [
    { value: "", label: "Todos" },
    { value: "borrador", label: "Borrador" },
    { value: "en_revision", label: "En Revisión" },
    { value: "aprobado", label: "Aprobado" },
    { value: "radicado", label: "Radicado" },
  ];

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Informes Semanales de Interventoría
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Formato GES-FO-016 v3 — Entrega: primer día hábil de cada semana
          </p>
        </div>
        <button
          onClick={handleGenerar}
          disabled={generando || !contratoId}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {generando ? "Generando..." : "+ Generar Informe"}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Filtros */}
      <div className="flex gap-4 mb-4">
        <select
          value={contratoId ?? ""}
          onChange={(e) => setContratoId(Number(e.target.value) || null)}
          className="border border-slate-300 rounded-lg px-3 py-2 text-sm"
        >
          <option value="">Seleccionar contrato</option>
          {contratos.map((c) => (
            <option key={c.id} value={c.id}>
              {c.numero} — {c.objeto.slice(0, 50)}
            </option>
          ))}
        </select>

        <div className="flex gap-1">
          {estados.map((e) => (
            <button
              key={e.value}
              onClick={() => setFiltroEstado(e.value)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filtroEstado === e.value
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {e.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tabla */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="text-left px-4 py-3 font-semibold text-slate-700">
                N.° Informe
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Periodo
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Avance Físico
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Estado
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Última Edición
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-4 py-12 text-center text-slate-400">
                  Cargando...
                </td>
              </tr>
            ) : informes.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-12 text-center text-slate-400">
                  No hay informes semanales registrados.
                  <br />
                  <span className="text-xs">
                    Usa el botón &quot;Generar Informe&quot; para crear el
                    borrador de la semana actual.
                  </span>
                </td>
              </tr>
            ) : (
              informes.map((inf) => (
                <tr
                  key={inf.id}
                  className="border-b border-slate-100 hover:bg-slate-50"
                >
                  <td className="px-4 py-3 font-medium">
                    Informe N.° {inf.numero_informe}
                  </td>
                  <td className="px-4 py-3 text-center text-slate-600">
                    {inf.semana_inicio} — {inf.semana_fin}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {Number(inf.avance_fisico_ejecutado).toFixed(1)}%
                  </td>
                  <td className="px-4 py-3 text-center">
                    <EstadoInformeBadge estado={inf.estado} />
                  </td>
                  <td className="px-4 py-3 text-center text-slate-500 text-xs">
                    {new Date(inf.updated_at).toLocaleDateString("es-CO")}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Link
                      href={`/informes/${inf.id}`}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Ver detalle →
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
