export interface Employee {
  id: number;
  full_name: string;
  job_title: string;
  department: string | null;
  country: string;
  salary: number;
  currency: string;
  employment_type: string;
  hire_date: string | null;
  is_active: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface EmployeeCreate {
  full_name: string;
  job_title: string;
  department?: string | null;
  country: string;
  salary: number;
  currency?: string;
  employment_type?: string;
  hire_date?: string | null;
}

export interface EmployeeUpdate {
  full_name?: string | null;
  job_title?: string | null;
  department?: string | null;
  country?: string | null;
  salary?: number | null;
  currency?: string | null;
  employment_type?: string | null;
  hire_date?: string | null;
}

export interface PaginatedEmployees {
  data: Employee[];
  total: number;
  limit: number;
  offset: number;
}

export interface CountryStats {
  country: string;
  headcount: number;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  median_salary: number;
  p25: number;
  p50: number;
  p75: number;
  p90: number;
}

export interface JobTitleStats {
  country: string;
  job_title: string;
  headcount: number;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  median_salary: number;
}

export interface GlobalSummary {
  total_employees: number;
  global_min_salary: number;
  global_max_salary: number;
  global_avg_salary: number;
  top_countries_by_headcount: { country: string; headcount: number }[];
  avg_salary_by_department: { department: string; avg_salary: number }[];
}

export interface InsightsFilters {
  countries: string[];
  job_titles: string[];
}