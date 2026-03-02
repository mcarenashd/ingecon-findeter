export default function DashboardPage() {
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
          value="4"
          subtitle="Supervisados"
          color="blue"
        />
        <KPICard
          label="Valor Interventoría"
          value="$4.407M"
          subtitle="COP — Precio Global Fijo"
          color="green"
        />
        <KPICard
          label="Hitos en Retraso"
          value="—"
          subtitle="Pendiente de datos"
          color="red"
        />
        <KPICard
          label="Informes Pendientes"
          value="—"
          subtitle="Pendiente de datos"
          color="yellow"
        />
      </div>

      {/* Placeholder sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Curva S — Avance Programado vs Ejecutado
          </h2>
          <div className="h-64 flex items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-lg">
            Gráfica de Curva S (próximamente)
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Semáforo de Hitos
          </h2>
          <div className="h-64 flex items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-lg">
            Tabla de hitos con semáforo (próximamente)
          </div>
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
