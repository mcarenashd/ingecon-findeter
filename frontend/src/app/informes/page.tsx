export default function InformesPage() {
  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Informes Semanales de Interventoría
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Formato GES-FO-016 v3 — Entrega: primer día hábil de cada semana
          </p>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
          + Nuevo Informe
        </button>
      </div>

      {/* Informes List */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="text-left px-4 py-3 font-semibold text-slate-700">
                N.° Informe
              </th>
              <th className="text-left px-4 py-3 font-semibold text-slate-700">
                Contrato
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
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                colSpan={6}
                className="px-4 py-12 text-center text-slate-400"
              >
                No hay informes semanales registrados.
                <br />
                <span className="text-xs">
                  Crea un contrato de obra primero para generar informes.
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Secciones del Informe */}
      <div className="mt-8 bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">
          Secciones del Informe Semanal (GES-FO-016)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            { num: 1, name: "Información General", auto: true },
            { num: 2, name: "Control de Hitos e Indicadores", auto: true },
            { num: 3, name: "Situaciones Problemáticas", auto: false },
            { num: 4, name: "Plan de Acción", auto: false },
            { num: 5, name: "Actividades No Previstas y Mayores Cantidades", auto: false },
            { num: 6, name: "Comentarios del Interventor", auto: false },
            { num: 7, name: "Registro Fotográfico", auto: false },
          ].map((s) => (
            <div
              key={s.num}
              className="flex items-center gap-3 p-3 rounded-lg border border-slate-100 hover:border-slate-300 transition-colors"
            >
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-700 text-sm font-bold">
                {s.num}
              </span>
              <div className="flex-1">
                <p className="text-sm font-medium text-slate-800">{s.name}</p>
                {s.auto && (
                  <p className="text-xs text-emerald-600">Autocompletado</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
