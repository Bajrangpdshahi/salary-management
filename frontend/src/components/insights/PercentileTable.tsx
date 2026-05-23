"use client";

import { formatSalary } from "@/lib/utils";

interface PercentileTableProps {
  p25: number;
  p50: number;
  p75: number;
  p90: number;
  currency?: string;
}

export function PercentileTable({
  p25,
  p50,
  p75,
  p90,
  currency = "USD",
}: PercentileTableProps) {
  const rows = [
    { label: "25th Percentile", value: p25 },
    { label: "50th Percentile (Median)", value: p50 },
    { label: "75th Percentile", value: p75 },
    { label: "90th Percentile", value: p90 },
  ];

  return (
    <div className="rounded-lg border bg-white">
      <div className="px-4 py-3 border-b">
        <h3 className="text-sm font-semibold text-gray-900">Salary Percentiles</h3>
      </div>
      <table className="w-full text-sm">
        <tbody>
          {rows.map((row) => (
            <tr key={row.label} className="border-b last:border-0">
              <td className="px-4 py-2.5 text-gray-600">{row.label}</td>
              <td className="px-4 py-2.5 text-right font-medium">
                {formatSalary(row.value, currency)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}