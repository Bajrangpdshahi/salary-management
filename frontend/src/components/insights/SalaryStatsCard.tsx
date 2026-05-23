"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingDown, TrendingUp, DollarSign } from "lucide-react";

interface SalaryStatsCardProps {
  title: string;
  value: number | null;
  currency?: string;
  icon: "min" | "max" | "avg" | "median";
}

const iconMap = {
  min: TrendingDown,
  max: TrendingUp,
  avg: DollarSign,
  median: DollarSign,
};

const colorMap = {
  min: "text-red-500",
  max: "text-green-500",
  avg: "text-blue-500",
  median: "text-purple-500",
};

export function SalaryStatsCard({
  title,
  value,
  currency = "USD",
  icon,
}: SalaryStatsCardProps) {
  const Icon = iconMap[icon];

  const formatted = value != null
    ? new Intl.NumberFormat("en-US", {
        style: "currency",
        currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value)
    : "—";

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-500">
          {title}
        </CardTitle>
        <Icon className={`h-4 w-4 ${colorMap[icon]}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatted}</div>
      </CardContent>
    </Card>
  );
}