"use client";

import { InsightsDashboard } from "@/components/insights/InsightsDashboard";

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Salary Insights</h1>
      <InsightsDashboard />
    </div>
  );
}