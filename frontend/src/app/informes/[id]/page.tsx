"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { apiFetch, apiDownload } from "@/lib/api";
import type {
  InformeSemanalDetail,
  AccionPlan,
  InformeFoto,
  ActividadNoPrevista,
  EstadoInforme,
} from "@/lib/types";
import { EstadoInformeBadge, EstadoHitoBadge, EstadoPlanBadge } from "@/components/EstadoBadge";

type Tab = "s1" | "s2" | "s3" | "s4" | "s5" | "s6" | "s7";

const TABS: { key: Tab; label: string; num: number }[] = [
  { key: "s1", label: "Info General", num: 1 },
  { key: "s2", label: "Hitos", num: 2 },
  { key: "s3", label: "Situaciones", num: 3 },
  { key: "s4", label: "Plan de Acción", num: 4 },
  { key: "s5", label: "Act. No Previstas", num: 5 },
  { key: "s6", label: "Comentarios", num: 6 },
  { key: "s7", label: "Fotos", num: 7 },
];

export default function InformeDetallePage() {
  const params = useParams();
  const router = useRouter();
  const informeId = Number(params.id);

  const [informe, setInforme] = useState<InformeSemanalDetail | null>(null);
  const [acciones, setAcciones] = useState<AccionPlan[]>([]);
  const [fotosInforme, setFotosInforme] = useState<InformeFoto[]>([]);
  const [actividadesNP, setActividadesNP] = useState<ActividadNoPrevista[]>([]);
  const [activeTab, setActiveTab] = useState<Tab>("s1");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const isBorrador = informe?.estado === "borrador";

  const loadInforme = useCallback(async () => {
    try {
      const data = await apiFetch<InformeSemanalDetail>(
        `/api/v1/informes/semanales/${informeId}`
      );
      setInforme(data);
    } catch {
      setError("Error cargando informe");
    }
  }, [informeId]);

  useEffect(() => {
    loadInforme();
  }, [loadInforme]);

  // Cargar datos secundarios cuando cambia el tab
  useEffect(() => {
    if (!informe) return;
    if (activeTab === "s4") {
      apiFetch<AccionPlan[]>(
        `/api/v1/informes/semanales/${informeId}/plan-accion`
      ).then(setAcciones).catch(() => {});
    }
    if (activeTab === "s7") {
      apiFetch<InformeFoto[]>(
        `/api/v1/informes/semanales/${informeId}/fotos`
      ).then(setFotosInforme).catch(() => {});
    }
    if (activeTab === "s5") {
      apiFetch<ActividadNoPrevista[]>(
        `/api/v1/contratos/obra/${informe.contrato_obra_id}/actividades-no-previstas`
      ).then(setActividadesNP).catch(() => {});
    }
  }, [activeTab, informe, informeId]);

  const saveSection = async (path: string, body: Record<string, unknown>) => {
    setSaving(true);
    setError(null);
    setSuccessMsg(null);
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/seccion/${path}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      });
      setSuccessMsg("Guardado exitosamente");
      await loadInforme();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al guardar");
    } finally {
      setSaving(false);
    }
  };

  const handleTransicion = async (nuevoEstado: EstadoInforme) => {
    setSaving(true);
    setError(null);
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/transicion`, {
        method: "POST",
        body: JSON.stringify({ nuevo_estado: nuevoEstado }),
      });
      await loadInforme();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error en transición");
    } finally {
      setSaving(false);
    }
  };

  const handleExportExcel = async () => {
    try {
      const blob = await apiDownload(
        `/api/v1/informes/semanales/${informeId}/exportar`
      );
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `GES-FO-016_Informe_${informe?.numero_informe}.xlsx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Error al exportar el informe a Excel.");
    }
  };

  if (!informe) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        Cargando informe...
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link
            href="/informes"
            className="text-slate-400 hover:text-slate-600 text-sm"
          >
            ← Volver
          </Link>
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Informe Semanal N.° {informe.numero_informe}
            </h1>
            <p className="text-sm text-slate-500">
              Periodo: {informe.semana_inicio} — {informe.semana_fin}
            </p>
          </div>
          <EstadoInformeBadge estado={informe.estado} />
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleExportExcel}
            className="border border-slate-300 text-slate-700 px-3 py-1.5 rounded-lg text-sm hover:bg-slate-50"
          >
            Exportar Excel
          </button>
          {informe.estado === "borrador" && (
            <button
              onClick={() => handleTransicion("en_revision")}
              disabled={saving}
              className="bg-blue-600 text-white px-3 py-1.5 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50"
            >
              Enviar a Revisión
            </button>
          )}
          {informe.estado === "en_revision" && (
            <>
              <button
                onClick={() => handleTransicion("borrador")}
                disabled={saving}
                className="border border-slate-300 text-slate-700 px-3 py-1.5 rounded-lg text-sm hover:bg-slate-50 disabled:opacity-50"
              >
                Devolver a Borrador
              </button>
              <button
                onClick={() => handleTransicion("aprobado")}
                disabled={saving}
                className="bg-emerald-600 text-white px-3 py-1.5 rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50"
              >
                Aprobar
              </button>
            </>
          )}
          {informe.estado === "aprobado" && (
            <button
              onClick={() => handleTransicion("radicado")}
              disabled={saving}
              className="bg-purple-600 text-white px-3 py-1.5 rounded-lg text-sm hover:bg-purple-700 disabled:opacity-50"
            >
              Radicar
            </button>
          )}
        </div>
      </div>

      {/* Mensajes */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      )}
      {successMsg && (
        <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-sm text-emerald-700">
          {successMsg}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 mb-4 border-b border-slate-200">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => {
              setActiveTab(tab.key);
              setError(null);
              setSuccessMsg(null);
            }}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.key
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            S{tab.num}. {tab.label}
          </button>
        ))}
      </div>

      {/* Contenido del tab activo */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        {activeTab === "s1" && <SeccionInfoGeneral informe={informe} />}
        {activeTab === "s2" && <SeccionHitos informe={informe} informeId={informeId} isBorrador={isBorrador} onRefresh={loadInforme} />}
        {activeTab === "s3" && <SeccionTexto label="Situaciones Problemáticas" field="situaciones_problematicas" value={informe.situaciones_problematicas} path="s3" isBorrador={isBorrador} saving={saving} onSave={saveSection} />}
        {activeTab === "s4" && <SeccionPlanAccion acciones={acciones} informeId={informeId} isBorrador={isBorrador} onReload={() => apiFetch<AccionPlan[]>(`/api/v1/informes/semanales/${informeId}/plan-accion`).then(setAcciones)} />}
        {activeTab === "s5" && <SeccionActividadesNP actividades={actividadesNP} narrativa={informe.actividades_no_previstas_narrativa} isBorrador={isBorrador} saving={saving} onSave={(body) => saveSection("s5", body)} />}
        {activeTab === "s6" && <SeccionComentarios informe={informe} isBorrador={isBorrador} saving={saving} onSave={saveSection} />}
        {activeTab === "s7" && <SeccionFotos fotos={fotosInforme} informeId={informeId} contratoId={informe.contrato_obra_id} isBorrador={isBorrador} onReload={() => apiFetch<InformeFoto[]>(`/api/v1/informes/semanales/${informeId}/fotos`).then(setFotosInforme)} />}
      </div>
    </div>
  );
}

// --- S1: Info General ---
function SeccionInfoGeneral({ informe }: { informe: InformeSemanalDetail }) {
  const fields = [
    { label: "N.° Informe", value: informe.numero_informe },
    { label: "Periodo", value: `${informe.semana_inicio} — ${informe.semana_fin}` },
    { label: "Avance Físico Programado", value: `${Number(informe.avance_fisico_programado).toFixed(2)}%` },
    { label: "Avance Físico Ejecutado", value: `${Number(informe.avance_fisico_ejecutado).toFixed(2)}%` },
    { label: "Valor Acum. Programado", value: `$${Number(informe.valor_acumulado_programado).toLocaleString("es-CO")}` },
    { label: "Valor Acum. Ejecutado", value: `$${Number(informe.valor_acumulado_ejecutado).toLocaleString("es-CO")}` },
    { label: "Creado", value: new Date(informe.created_at).toLocaleDateString("es-CO") },
  ];

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección 1 — Información General</h3>
      <p className="text-xs text-emerald-600 mb-4">Autocompletado desde el módulo de contratos</p>
      <div className="grid grid-cols-2 gap-4">
        {fields.map((f) => (
          <div key={f.label} className="p-3 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-500">{f.label}</p>
            <p className="font-medium text-slate-900">{f.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// --- S2: Hitos ---
function SeccionHitos({ informe, informeId, isBorrador, onRefresh }: {
  informe: InformeSemanalDetail;
  informeId: number;
  isBorrador: boolean;
  onRefresh: () => void;
}) {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/refresh-snapshot`, {
        method: "POST",
      });
      onRefresh();
    } catch { /* ignore */ }
    setRefreshing(false);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-slate-900">Sección 2 — Control de Hitos</h3>
          <p className="text-xs text-emerald-600">Snapshot al momento de generar el informe</p>
        </div>
        {isBorrador && (
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="text-sm text-blue-600 hover:text-blue-800 disabled:opacity-50"
          >
            {refreshing ? "Actualizando..." : "Actualizar Snapshot"}
          </button>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 border-b">
              <th className="text-left px-3 py-2 font-semibold text-slate-600">N.°</th>
              <th className="text-left px-3 py-2 font-semibold text-slate-600">Descripción</th>
              <th className="text-center px-3 py-2 font-semibold text-slate-600">F. Programada</th>
              <th className="text-center px-3 py-2 font-semibold text-slate-600">F. Real</th>
              <th className="text-center px-3 py-2 font-semibold text-slate-600">Avance</th>
              <th className="text-center px-3 py-2 font-semibold text-slate-600">Días Retraso</th>
              <th className="text-center px-3 py-2 font-semibold text-slate-600">Estado</th>
            </tr>
          </thead>
          <tbody>
            {informe.snapshot_hitos.map((h) => (
              <tr key={h.id} className="border-b border-slate-100">
                <td className="px-3 py-2">{h.numero}</td>
                <td className="px-3 py-2 max-w-xs truncate">{h.descripcion}</td>
                <td className="px-3 py-2 text-center text-slate-600">{h.fecha_programada}</td>
                <td className="px-3 py-2 text-center text-slate-600">{h.fecha_real ?? "—"}</td>
                <td className="px-3 py-2 text-center">{Number(h.avance_porcentaje).toFixed(1)}%</td>
                <td className={`px-3 py-2 text-center font-medium ${h.dias_retraso > 30 ? "text-red-600" : h.dias_retraso > 0 ? "text-amber-600" : "text-emerald-600"}`}>
                  {h.dias_retraso}
                </td>
                <td className="px-3 py-2 text-center">
                  <EstadoHitoBadge estado={h.estado} />
                </td>
              </tr>
            ))}
            {informe.snapshot_hitos.length === 0 && (
              <tr>
                <td colSpan={7} className="px-3 py-8 text-center text-slate-400">
                  Sin hitos registrados
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// --- S3/S5 generic text editor ---
function SeccionTexto({ label, field, value, path, isBorrador, saving, onSave }: {
  label: string;
  field: string;
  value: string | null;
  path: string;
  isBorrador: boolean;
  saving: boolean;
  onSave: (path: string, body: Record<string, unknown>) => void;
}) {
  const [text, setText] = useState(value ?? "");

  useEffect(() => { setText(value ?? ""); }, [value]);

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección {path.replace("s", "")} — {label}</h3>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={!isBorrador}
        rows={8}
        className="w-full border border-slate-300 rounded-lg p-3 text-sm resize-y disabled:bg-slate-50 disabled:text-slate-500"
        placeholder={`Escribir ${label.toLowerCase()}...`}
      />
      {isBorrador && (
        <button
          onClick={() => onSave(path, { [field]: text || null })}
          disabled={saving}
          className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Guardando..." : "Guardar"}
        </button>
      )}
    </div>
  );
}

// --- S4: Plan de Acción ---
function SeccionPlanAccion({ acciones, informeId, isBorrador, onReload }: {
  acciones: AccionPlan[];
  informeId: number;
  isBorrador: boolean;
  onReload: () => void;
}) {
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState({ actividad: "", responsable: "", fecha_programada: "" });

  const handleAdd = async () => {
    if (!form.actividad || !form.responsable || !form.fecha_programada) return;
    setAdding(true);
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/plan-accion`, {
        method: "POST",
        body: JSON.stringify(form),
      });
      setForm({ actividad: "", responsable: "", fecha_programada: "" });
      onReload();
    } catch { /* ignore */ }
    setAdding(false);
  };

  const handleUpdateEstado = async (accionId: number, estado: string) => {
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/plan-accion/${accionId}`, {
        method: "PATCH",
        body: JSON.stringify({ estado }),
      });
      onReload();
    } catch { /* ignore */ }
  };

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección 4 — Plan de Acción</h3>

      <table className="w-full text-sm mb-4">
        <thead>
          <tr className="bg-slate-50 border-b">
            <th className="text-left px-3 py-2 font-semibold text-slate-600">N.°</th>
            <th className="text-left px-3 py-2 font-semibold text-slate-600">Actividad</th>
            <th className="text-left px-3 py-2 font-semibold text-slate-600">Responsable</th>
            <th className="text-center px-3 py-2 font-semibold text-slate-600">F. Programada</th>
            <th className="text-center px-3 py-2 font-semibold text-slate-600">Estado</th>
            <th className="text-left px-3 py-2 font-semibold text-slate-600">Observaciones</th>
          </tr>
        </thead>
        <tbody>
          {acciones.map((a) => (
            <tr key={a.id} className="border-b border-slate-100">
              <td className="px-3 py-2">{a.numero}</td>
              <td className="px-3 py-2 max-w-xs">{a.actividad}</td>
              <td className="px-3 py-2">{a.responsable}</td>
              <td className="px-3 py-2 text-center text-slate-600">{a.fecha_programada}</td>
              <td className="px-3 py-2 text-center">
                {isBorrador ? (
                  <select
                    value={a.estado}
                    onChange={(e) => handleUpdateEstado(a.id, e.target.value)}
                    className="text-xs border border-slate-300 rounded px-1 py-0.5"
                  >
                    <option value="pendiente">Pendiente</option>
                    <option value="en_proceso">En Proceso</option>
                    <option value="cumplido">Cumplido</option>
                    <option value="vencido">Vencido</option>
                  </select>
                ) : (
                  <EstadoPlanBadge estado={a.estado} />
                )}
              </td>
              <td className="px-3 py-2 text-slate-500 text-xs">{a.observaciones ?? "—"}</td>
            </tr>
          ))}
          {acciones.length === 0 && (
            <tr>
              <td colSpan={6} className="px-3 py-8 text-center text-slate-400">
                Sin acciones registradas
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {isBorrador && (
        <div className="flex gap-2 items-end">
          <input
            placeholder="Actividad"
            value={form.actividad}
            onChange={(e) => setForm({ ...form, actividad: e.target.value })}
            className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm"
          />
          <input
            placeholder="Responsable"
            value={form.responsable}
            onChange={(e) => setForm({ ...form, responsable: e.target.value })}
            className="w-40 border border-slate-300 rounded-lg px-3 py-2 text-sm"
          />
          <input
            type="date"
            value={form.fecha_programada}
            onChange={(e) => setForm({ ...form, fecha_programada: e.target.value })}
            className="border border-slate-300 rounded-lg px-3 py-2 text-sm"
          />
          <button
            onClick={handleAdd}
            disabled={adding}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50 whitespace-nowrap"
          >
            + Agregar
          </button>
        </div>
      )}
    </div>
  );
}

// --- S5: Actividades No Previstas ---
function SeccionActividadesNP({ actividades, narrativa, isBorrador, saving, onSave }: {
  actividades: ActividadNoPrevista[];
  narrativa: string | null;
  isBorrador: boolean;
  saving: boolean;
  onSave: (body: Record<string, unknown>) => void;
}) {
  const [text, setText] = useState(narrativa ?? "");
  useEffect(() => { setText(narrativa ?? ""); }, [narrativa]);

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección 5 — Actividades No Previstas y Mayores Cantidades</h3>

      <table className="w-full text-sm mb-6">
        <thead>
          <tr className="bg-slate-50 border-b">
            <th className="text-left px-3 py-2 font-semibold text-slate-600">Código</th>
            <th className="text-left px-3 py-2 font-semibold text-slate-600">Descripción</th>
            <th className="text-center px-3 py-2 font-semibold text-slate-600">F. Programada</th>
            <th className="text-center px-3 py-2 font-semibold text-slate-600">F. Real</th>
          </tr>
        </thead>
        <tbody>
          {actividades.map((a) => (
            <tr key={a.id} className="border-b border-slate-100">
              <td className="px-3 py-2 font-mono text-xs">{a.codigo}</td>
              <td className="px-3 py-2">{a.descripcion}</td>
              <td className="px-3 py-2 text-center text-slate-600">{a.fecha_programada ?? "—"}</td>
              <td className="px-3 py-2 text-center text-slate-600">{a.fecha_real ?? "—"}</td>
            </tr>
          ))}
          {actividades.length === 0 && (
            <tr>
              <td colSpan={4} className="px-3 py-6 text-center text-slate-400">
                Sin actividades no previstas registradas
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <h4 className="font-medium text-slate-700 mb-2">Narrativa</h4>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={!isBorrador}
        rows={5}
        className="w-full border border-slate-300 rounded-lg p-3 text-sm resize-y disabled:bg-slate-50"
        placeholder="Describir actividades no previstas y mayores cantidades..."
      />
      {isBorrador && (
        <button
          onClick={() => onSave({ actividades_no_previstas_narrativa: text || null })}
          disabled={saving}
          className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Guardando..." : "Guardar Narrativa"}
        </button>
      )}
    </div>
  );
}

// --- S6: Comentarios ---
function SeccionComentarios({ informe, isBorrador, saving, onSave }: {
  informe: InformeSemanalDetail;
  isBorrador: boolean;
  saving: boolean;
  onSave: (path: string, body: Record<string, unknown>) => void;
}) {
  const bloques = [
    { key: "tecnico", label: "Comentario Técnico", field: "comentario_tecnico", path: "s6-tecnico", value: informe.comentario_tecnico },
    { key: "sst", label: "Comentario SST", field: "comentario_sst", path: "s6-sst", value: informe.comentario_sst },
    { key: "ambiental", label: "Comentario Ambiental", field: "comentario_ambiental", path: "s6-ambiental", value: informe.comentario_ambiental },
    { key: "social", label: "Comentario Social", field: "comentario_social", path: "s6-social", value: informe.comentario_social },
  ];

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección 6 — Comentarios del Interventor</h3>
      <div className="space-y-6">
        {bloques.map((b) => (
          <BloqueComentario
            key={b.key}
            label={b.label}
            field={b.field}
            path={b.path}
            value={b.value}
            isBorrador={isBorrador}
            saving={saving}
            onSave={onSave}
          />
        ))}
      </div>
    </div>
  );
}

function BloqueComentario({ label, field, path, value, isBorrador, saving, onSave }: {
  label: string;
  field: string;
  path: string;
  value: string | null;
  isBorrador: boolean;
  saving: boolean;
  onSave: (path: string, body: Record<string, unknown>) => void;
}) {
  const [text, setText] = useState(value ?? "");
  useEffect(() => { setText(value ?? ""); }, [value]);

  return (
    <div className="border border-slate-200 rounded-lg p-4">
      <h4 className="font-medium text-slate-700 mb-2">{label}</h4>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={!isBorrador}
        rows={4}
        className="w-full border border-slate-300 rounded-lg p-3 text-sm resize-y disabled:bg-slate-50"
        placeholder={`Escribir ${label.toLowerCase()}...`}
      />
      {isBorrador && (
        <button
          onClick={() => onSave(path, { [field]: text || null })}
          disabled={saving}
          className="mt-2 bg-blue-600 text-white px-3 py-1.5 rounded-lg text-xs hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Guardando..." : "Guardar"}
        </button>
      )}
    </div>
  );
}

// --- S7: Fotos ---
function SeccionFotos({ fotos, informeId, contratoId, isBorrador, onReload }: {
  fotos: InformeFoto[];
  informeId: number;
  contratoId: number;
  isBorrador: boolean;
  onReload: () => void;
}) {
  const [bancoFotos, setBancoFotos] = useState<import("@/lib/types").Foto[]>([]);

  useEffect(() => {
    apiFetch<import("@/lib/types").Foto[]>(
      `/api/v1/fotos?contrato_obra_id=${contratoId}`
    ).then(setBancoFotos).catch(() => {});
  }, [contratoId]);

  const fotosEnInforme = new Set(fotos.map((f) => f.foto_id));

  const handleAgregar = async (fotoId: number) => {
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/fotos`, {
        method: "POST",
        body: JSON.stringify({ foto_id: fotoId, orden: fotos.length + 1 }),
      });
      onReload();
    } catch { /* ignore */ }
  };

  const handleRemover = async (informeFotoId: number) => {
    try {
      await apiFetch(`/api/v1/informes/semanales/${informeId}/fotos/${informeFotoId}`, {
        method: "DELETE",
      });
      onReload();
    } catch { /* ignore */ }
  };

  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-4">Sección 7 — Registro Fotográfico</h3>

      <div className="grid grid-cols-2 gap-6">
        {/* Fotos del informe */}
        <div>
          <h4 className="font-medium text-slate-700 mb-3">
            Fotos del Informe ({fotos.length})
          </h4>
          <div className="space-y-3">
            {fotos.map((f) => (
              <div
                key={f.id}
                className="flex items-center gap-3 p-3 border border-slate-200 rounded-lg"
              >
                <div className="w-16 h-16 bg-slate-100 rounded flex items-center justify-center text-xs text-slate-400 overflow-hidden">
                  <img
                    src={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/fotos/${f.foto_id}/archivo`}
                    alt={f.pie_de_foto_override || f.foto.pie_de_foto || ""}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">
                    {f.pie_de_foto_override || f.foto.pie_de_foto || f.foto.archivo_nombre}
                  </p>
                  <p className="text-xs text-slate-500">{f.foto.fecha_toma}</p>
                </div>
                {isBorrador && (
                  <button
                    onClick={() => handleRemover(f.id)}
                    className="text-red-500 hover:text-red-700 text-xs"
                  >
                    Quitar
                  </button>
                )}
              </div>
            ))}
            {fotos.length === 0 && (
              <p className="text-sm text-slate-400 text-center py-6">
                Sin fotos seleccionadas
              </p>
            )}
          </div>
        </div>

        {/* Banco de fotos */}
        <div>
          <h4 className="font-medium text-slate-700 mb-3">
            Banco de Fotos ({bancoFotos.length})
          </h4>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {bancoFotos
              .filter((f) => !fotosEnInforme.has(f.id))
              .map((f) => (
                <div
                  key={f.id}
                  className="flex items-center gap-3 p-2 border border-slate-100 rounded-lg hover:border-slate-300"
                >
                  <div className="w-12 h-12 bg-slate-100 rounded overflow-hidden">
                    <img
                      src={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/fotos/${f.id}/archivo`}
                      alt={f.pie_de_foto || ""}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium truncate">
                      {f.pie_de_foto || f.archivo_nombre}
                    </p>
                    <p className="text-xs text-slate-400">{f.fecha_toma}</p>
                  </div>
                  {isBorrador && (
                    <button
                      onClick={() => handleAgregar(f.id)}
                      className="text-blue-600 hover:text-blue-800 text-xs whitespace-nowrap"
                    >
                      + Agregar
                    </button>
                  )}
                </div>
              ))}
            {bancoFotos.filter((f) => !fotosEnInforme.has(f.id)).length === 0 && (
              <p className="text-sm text-slate-400 text-center py-6">
                No hay fotos disponibles en el banco
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
