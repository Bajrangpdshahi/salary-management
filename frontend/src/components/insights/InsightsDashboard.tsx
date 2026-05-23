"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { insightsApi } from "@/lib/api";
import { SalaryStatsCard } from "./SalaryStatsCard";
import { PercentileTable } from "./PercentileTable";
import { SalaryBarChart } from "./SalaryBarChart";

export function InsightsDashboard() {
  const [country, setCountry] = useState("");
  const [jobTitle, setJobTitle] = useState("");

  // Fetch distinct filter values from the database
  const { data: filters } = useQuery({
    queryKey: ["insights", "filters"],
    queryFn: () => insightsApi.filters(),
  });

  const { data: countryStats, isLoading: countryLoading } = useQuery({
    queryKey: ["insights", "country", country],
    queryFn: () => insightsApi.countryStats(country),
    enabled: !!country,
  });

  const { data: jobTitleStats, isLoading: jobTitleLoading } = useQuery({
    queryKey: ["insights", "job-title", country || "global", jobTitle],
    queryFn: () => insightsApi.jobTitleStats(jobTitle, country || undefined),
    enabled: !!jobTitle,
  });

  const { data: summary } = useQuery({
    queryKey: ["insights", "summary"],
    queryFn: () => insightsApi.summary(),
  });

  const selectClass =
    "flex h-10 w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-950";

  return (
    <div className="space-y-6">
      {/* Global Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="rounded-lg border bg-white p-4">
            <p className="text-sm text-gray-500">Total Employees</p>
            <p className="text-2xl font-bold">{summary.total_employees.toLocaleString()}</p>
          </div>
          <SalaryStatsCard
            title="Global Min Salary"
            value={summary.global_min_salary}
            icon="min"
          />
          <SalaryStatsCard
            title="Global Max Salary"
            value={summary.global_max_salary}
            icon="max"
          />
          <SalaryStatsCard
            title="Global Avg Salary"
            value={summary.global_avg_salary}
            icon="avg"
          />
        </div>
      )}

      {/* Filters — native <select> matching EmployeeForm convention */}
      <div className="flex gap-4 items-end">
        <div className="space-y-2">
          <label htmlFor="insights-country" className="text-sm font-medium">
            Country
          </label>
          <select
            id="insights-country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className={selectClass}
          >
            <option value="">Select country...</option>
            {(filters?.countries ?? []).map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-2">
          <label htmlFor="insights-job-title" className="text-sm font-medium">
            Job Title
          </label>
          <select
            id="insights-job-title"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            className={selectClass}
          >
            <option value="">Select job title...</option>
            {(filters?.job_titles ?? []).map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Country Stats */}
      {country && countryStats && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">
            {country} — {countryStats.headcount.toLocaleString()} employees
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <SalaryStatsCard title="Min Salary" value={countryStats.min_salary} icon="min" />
            <SalaryStatsCard title="Max Salary" value={countryStats.max_salary} icon="max" />
            <SalaryStatsCard title="Avg Salary" value={countryStats.avg_salary} icon="avg" />
            <SalaryStatsCard title="Median Salary" value={countryStats.median_salary} icon="median" />
          </div>
          <PercentileTable
            p25={countryStats.p25}
            p50={countryStats.p50}
            p75={countryStats.p75}
            p90={countryStats.p90}
          />
        </div>
      )}

      {/* Job Title Stats */}
      {jobTitle && jobTitleStats && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">
            {jobTitle} {country ? `in ${country}` : "(Global)"} — {jobTitleStats.headcount.toLocaleString()} employees
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <SalaryStatsCard title="Min Salary" value={jobTitleStats.min_salary} icon="min" />
            <SalaryStatsCard title="Max Salary" value={jobTitleStats.max_salary} icon="max" />
            <SalaryStatsCard title="Avg Salary" value={jobTitleStats.avg_salary} icon="avg" />
            <SalaryStatsCard title="Median Salary" value={jobTitleStats.median_salary} icon="median" />
          </div>
        </div>
      )}

      {/* Bar Charts from Global Summary */}
      {summary && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SalaryBarChart
            title="Top Countries by Headcount"
            data={summary.top_countries_by_headcount.map((c) => ({
              label: c.country,
              value: c.headcount,
            }))}
            barColor="#3b82f6"
          />
          <SalaryBarChart
            title="Avg Salary by Department"
            data={summary.avg_salary_by_department.map((d) => ({
              label: d.department,
              value: d.avg_salary,
            }))}
            barColor="#8b5cf6"
          />
        </div>
      )}
    </div>
  );
}