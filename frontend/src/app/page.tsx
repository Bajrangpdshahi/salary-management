import Link from "next/link";
import { ArrowRight, Users, BarChart3 } from "lucide-react";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Salary Management Tool
      </h1>
      <p className="text-lg text-gray-500 max-w-md mb-8">
        Manage 10,000+ employee records with powerful search, pagination,
        and salary analytics at your fingertips.
      </p>
      <div className="flex gap-4">
        <Link
          href="/employees"
          className="inline-flex items-center gap-2 rounded-lg bg-gray-900 px-6 py-3 text-sm font-medium text-white hover:bg-gray-800 transition-colors"
        >
          <Users className="h-4 w-4" />
          View Employees
          <ArrowRight className="h-4 w-4" />
        </Link>
        <Link
          href="/insights"
          className="inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-6 py-3 text-sm font-medium text-gray-900 hover:bg-gray-50 transition-colors"
        >
          <BarChart3 className="h-4 w-4" />
          Salary Insights
        </Link>
      </div>
    </div>
  );
}