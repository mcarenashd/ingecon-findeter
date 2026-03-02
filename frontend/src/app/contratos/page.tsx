import Link from "next/link";

const contratos = [
  {
    id: 1,
    proyecto: "Proyecto 1 — Puentes Vehiculares y Peatonales",
    descripcion:
      "Conservación de puentes vehiculares y/o peatonales sobre cuerpos de agua y ciclo infraestructura",
    contrato: "Pendiente asignación",
    contratista: "Pendiente adjudicación",
    valor: null,
    plazo: "10 meses",
    plazoEtapa1: "2 meses",
    plazoEtapa2: "8 meses",
    hitos: null,
    estado: "etapa1" as const,
  },
  {
    id: 2,
    proyecto: "Proyecto 2 — Espacio Público",
    descripcion:
      "Conservación del espacio público en la localidad de Bosa",
    contrato: "Pendiente asignación",
    contratista: "Pendiente adjudicación",
    valor: null,
    plazo: "12 meses",
    plazoEtapa1: "2 meses",
    plazoEtapa2: "10 meses",
    hitos: null,
    estado: "etapa1" as const,
  },
  {
    id: 3,
    proyecto: "Proyecto 3 — Malla Vial",
    descripcion:
      "Construcción y rehabilitación/conservación de malla vial y espacio público asociado",
    contrato: "Pendiente asignación",
    contratista: "Pendiente adjudicación",
    valor: null,
    plazo: "12 meses",
    plazoEtapa1: "2 meses",
    plazoEtapa2: "10 meses",
    hitos: null,
    estado: "etapa1" as const,
  },
  {
    id: 4,
    proyecto: "Proyecto 4 — Parques y Espacio Público",
    descripcion:
      "Obras y actividades necesarias para la construcción de parques y espacio público asociado",
    contrato: "CTO 703-2024",
    contratista: "Consorcio Infraestructura Bosa",
    valor: "$4.462.324.289",
    plazo: "10 meses",
    plazoEtapa1: "1 mes",
    plazoEtapa2: "9 meses",
    hitos: 20,
    estado: "ejecucion" as const,
    parques: [
      { nombre: "Parque La Esperanza 7-236", hitos: 20, estado: "retraso" as const },
      { nombre: "Parque Piamonte 7-145", hitos: 20, estado: "ejecucion" as const },
    ],
  },
];

const estadoBadge = {
  etapa1: "bg-blue-100 text-blue-700",
  ejecucion: "bg-emerald-100 text-emerald-700",
  retraso: "bg-red-100 text-red-700",
};

const estadoLabel = {
  etapa1: "Etapa I — Estudios y Diseños",
  ejecucion: "Etapa II — Ejecución",
  retraso: "En Retraso",
};

export default function ContratosPage() {
  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Gestión de Contratos de Obra
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            4 proyectos supervisados bajo interventoría FDT-ATBOSA-I-028-2025
          </p>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
          + Nuevo Contrato
        </button>
      </div>

      {/* Contracts Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="text-left px-4 py-3 font-semibold text-slate-700">
                Proyecto / Contrato
              </th>
              <th className="text-left px-4 py-3 font-semibold text-slate-700">
                Contratista
              </th>
              <th className="text-right px-4 py-3 font-semibold text-slate-700">
                Valor (COP)
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Plazo
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Estado
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            {contratos.map((c) => (
              <tr
                key={c.id}
                className="border-b border-slate-100 hover:bg-slate-50"
              >
                <td className="px-4 py-3">
                  <div className="font-medium text-slate-900">
                    {c.proyecto}
                  </div>
                  <div className="text-xs text-slate-500 mt-0.5">
                    {c.contrato}
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">
                    {c.descripcion}
                  </div>
                  {"parques" in c && c.parques && (
                    <div className="mt-1.5 flex flex-wrap gap-1">
                      {c.parques.map((p) => (
                        <span
                          key={p.nombre}
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            p.estado === "retraso"
                              ? "bg-red-50 text-red-600"
                              : "bg-emerald-50 text-emerald-600"
                          }`}
                        >
                          {p.nombre} — {p.hitos} hitos
                        </span>
                      ))}
                    </div>
                  )}
                </td>
                <td className="px-4 py-3 text-slate-600">
                  {c.contratista}
                </td>
                <td className="px-4 py-3 text-right font-mono text-slate-700">
                  {c.valor ?? "—"}
                </td>
                <td className="px-4 py-3 text-center text-slate-600">
                  <div>{c.plazo}</div>
                  <div className="text-xs text-slate-400">
                    E1: {c.plazoEtapa1} / E2: {c.plazoEtapa2}
                  </div>
                </td>
                <td className="px-4 py-3 text-center">
                  <span
                    className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${estadoBadge[c.estado]}`}
                  >
                    {estadoLabel[c.estado]}
                  </span>
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
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
