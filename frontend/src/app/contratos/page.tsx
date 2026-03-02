import Link from "next/link";

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
            Contratos supervisados bajo FDT-ATBOSA-I-028-2025
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
                Contrato
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
                Hitos
              </th>
              <th className="text-center px-4 py-3 font-semibold text-slate-700">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-slate-100 hover:bg-slate-50">
              <td className="px-4 py-3">
                <div className="font-medium text-slate-900">
                  Parque La Esperanza 7-236
                </div>
                <div className="text-xs text-slate-500">CTO 703</div>
              </td>
              <td className="px-4 py-3 text-slate-600">
                Consorcio Infraestructura Bosa
              </td>
              <td className="px-4 py-3 text-right font-mono text-slate-700">
                $4.462.000.000
              </td>
              <td className="px-4 py-3 text-center text-slate-600">240 días</td>
              <td className="px-4 py-3 text-center">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700">
                  20 hitos
                </span>
              </td>
              <td className="px-4 py-3 text-center">
                <Link
                  href="/contratos/1"
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Ver detalle
                </Link>
              </td>
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50">
              <td className="px-4 py-3">
                <div className="font-medium text-slate-900">
                  Parque Piamonte 7-145
                </div>
                <div className="text-xs text-slate-500">CTO 703</div>
              </td>
              <td className="px-4 py-3 text-slate-600">
                Consorcio Infraestructura Bosa
              </td>
              <td className="px-4 py-3 text-right font-mono text-slate-700">—</td>
              <td className="px-4 py-3 text-center text-slate-600">240 días</td>
              <td className="px-4 py-3 text-center">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700">
                  20 hitos
                </span>
              </td>
              <td className="px-4 py-3 text-center">
                <Link
                  href="/contratos/2"
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Ver detalle
                </Link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
