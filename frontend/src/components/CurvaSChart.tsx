"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { CurvaSDataPoint } from "@/lib/types";

interface CurvaSChartProps {
  data: CurvaSDataPoint[];
  height?: number;
}

function CustomTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: { value: number; dataKey: string; color: string }[];
  label?: number;
}) {
  if (!active || !payload || payload.length === 0) return null;

  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-lg px-3 py-2 text-xs">
      <p className="font-semibold text-slate-700 mb-1">Semana {label}</p>
      {payload.map((entry) => (
        <p key={entry.dataKey} style={{ color: entry.color }}>
          {entry.dataKey === "programado" ? "Programado" : "Ejecutado"}:{" "}
          <span className="font-medium">{Number(entry.value).toFixed(1)}%</span>
        </p>
      ))}
    </div>
  );
}

export function CurvaSChart({ data, height = 250 }: CurvaSChartProps) {
  if (data.length < 2) {
    return (
      <div
        className="flex items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-lg text-sm"
        style={{ height }}
      >
        Sin datos suficientes para generar la Curva S
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart
        data={data}
        margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis
          dataKey="semana"
          tick={{ fontSize: 12, fill: "#64748b" }}
          tickFormatter={(v) => `S${v}`}
        />
        <YAxis
          domain={[0, 100]}
          tick={{ fontSize: 12, fill: "#64748b" }}
          tickFormatter={(v) => `${v}%`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          formatter={(value) =>
            value === "programado" ? "Programado" : "Ejecutado"
          }
          wrapperStyle={{ fontSize: 12 }}
        />
        <Line
          type="monotone"
          dataKey="programado"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ r: 3, fill: "#3b82f6" }}
          activeDot={{ r: 5 }}
        />
        <Line
          type="monotone"
          dataKey="ejecutado"
          stroke="#f97316"
          strokeWidth={2}
          dot={{ r: 3, fill: "#f97316" }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
