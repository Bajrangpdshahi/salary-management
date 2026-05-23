"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { insightsApi } from "@/lib/api";
import { SalaryStatsCard } from "./SalaryStatsCard";
import { PercentileTable } from "./PercentileTable";
import { SalaryBarChart } from "./SalaryBarChart";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const COUNTRIES = [
  "USA", "Canada", "UK", "Germany", "France",
  "Spain", "Italy", "Netherlands", "Sweden", "Denmark",
  "India", "China", "Japan", "South Korea", "Australia",
  "Brazil", "Mexico", "Argentina", "Singapore", "UAE",
];

const JOB_TITLES = [
  "Software Engineer", "Senior Software Engineer", "Engineering Manager",
  "Data Analyst", "Data Scientist", "Senior Data Scientist",
  "Product Manager", "Senior Product Manager", "UX Designer",
  "DevOps Engineer", "Cloud Architect", "QA Engineer",
  "HR Manager", "Financial Analyst", "Marketing Manager",
  "Sales Executive", "Operations Manager", "Customer Success Manager",
  "Technical Writer", "Security Engineer",
];

export function InsightsDashboard() {
  const [country, setCountry] = useState("");
  const [jobTitle, setJobTitle] = useState("");

  const { data: countryStats, isLoading: countryLoading } = useQuery({
    queryKey: ["insights", "country", country],
    queryFn: () => insightsApi.countryStats(country),
    enabled: !!country,
  });

  const { data: jobTitleStats, isLoading: jobTitleLoading } = useQuery({
    queryKey: ["insights", "job-title", country, jobTitle],
    queryFn: () => insightsApi.jobTitleStats(country, jobTitle),
    enabled: !!country && !!jobTitle,
  });

  const { data: summary } = useQuery({
    queryKey: ["insights", "summary"],
    queryFn: () => insightsApi.summary(),
  });

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

      {/* Filters */}
      <div className="flex gap-4">
        <div className="w-[200px]">
          <label className="text-sm font-medium text-gray-600 mb-1 block">
            Country
          </label>
          <Select value={country} onValueChange={(v) => { setCountry(v); setJobTitle(""); }}>
            <SelectTrigger>
              <SelectValue placeholder="Select country..." />
            </SelectTrigger>
            <SelectContent>
              {COUNTRIES.map((c) => (
                <SelectItem key={c} value={c}>{c}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="w-[220px]">
          <label className="text-sm font-medium text-gray-600 mb-1 block">
            Job Title
          </label>
          <Select value={jobTitle} onValueChange={setJobTitle} key={country}>
            <SelectTrigger>
              <SelectValue placeholder="Select job title..." />
            </SelectTrigger>
            <SelectContent>
              {JOB_TITLES.map((t) => (
                <SelectItem key={t} value={t}>{t}</SelectItem>
              ))}
            </SelectContent>
          </Select>
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
      {country && jobTitle && jobTitleStats && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">
            {jobTitle} in {country} — {jobTitleStats.headcount.toLocaleString()} employees
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