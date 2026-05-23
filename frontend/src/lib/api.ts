import axios from "axios";
import type {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  PaginatedEmployees,
  CountryStats,
  JobTitleStats,
  GlobalSummary,
  InsightsFilters,
} from "@/types/employee";

// Empty baseURL uses Next.js rewrites proxy — no CORS issues
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "",
});

export const employeesApi = {
  list: (params: {
    limit?: number;
    offset?: number;
    search?: string;
    country?: string;
  }) =>
    api.get<PaginatedEmployees>("/api/employees", { params }).then((r) => r.data),

  get: (id: number) =>
    api.get<Employee>(`/api/employees/${id}`).then((r) => r.data),

  create: (data: EmployeeCreate) =>
    api.post<Employee>("/api/employees", data).then((r) => r.data),

  update: (id: number, data: EmployeeUpdate) =>
    api.put<Employee>(`/api/employees/${id}`, data).then((r) => r.data),

  delete: (id: number) => api.delete(`/api/employees/${id}`),
};

export const insightsApi = {
  filters: () =>
    api.get<InsightsFilters>("/api/insights/filters").then((r) => r.data),

  countryStats: (country: string) =>
    api
      .get<CountryStats>(`/api/insights/country/${country}`)
      .then((r) => r.data),

  jobTitleStats: (country: string, jobTitle: string) =>
    api
      .get<JobTitleStats>("/api/insights/job-title", {
        params: { country, job_title: jobTitle },
      })
      .then((r) => r.data),

  summary: () =>
    api.get<GlobalSummary>("/api/insights/summary").then((r) => r.data),
};