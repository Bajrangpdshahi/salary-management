"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { formatSalary } from "@/lib/utils";

interface SalaryBarChartProps {
  data: { label: string; value: number }[];
  title: string;
  currency?: string;
  barColor?: string;
}

export function SalaryBarChart({
  data,
  title,
  currency = "USD",
  barColor = "#6366f1",
}: SalaryBarChartProps) {
  if (data.length === 0) {
    return (
      <div className="rounded-lg border bg-white p-8 text-center text-gray-500">
        No data available
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white p-4">
      <h3 className="text-sm font-semibold text-gray-900 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart
          data={data}
          margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="label"
            tick={{ fontSize: 12, fill: "#6b7280" }}
            tickLine={false}
            angle={-30}
            textAnchor="end"
            height={60}
          />
          <YAxis
            tick={{ fontSize: 12, fill: "#6b7280" }}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) =>
              new Intl.NumberFormat("en-US", {
                style: "currency",
                currency,
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
              }).format(v)
            }
          />
          <Tooltip
            formatter={(value: number) => [formatSalary(value, currency), ""]}
            contentStyle={{
              fontSize: "12px",
              borderRadius: "6px",
              border: "1px solid #e5e7eb",
            }}
          />
          <Bar dataKey="value" fill={barColor} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}