"use client";

import { useQuery } from "@tanstack/react-query";
import { employeesApi } from "@/lib/api";
import { formatSalary, formatDate } from "@/lib/utils";
import type { Employee } from "@/types/employee";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Pencil, Trash2, ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";

const PAGE_SIZE = 20;

interface EmployeeTableProps {
  search: string;
  country: string;
  onEdit: (employee: Employee) => void;
  onDelete: (employee: Employee) => void;
}

export function EmployeeTable({
  search,
  country,
  onEdit,
  onDelete,
}: EmployeeTableProps) {
  const [offset, setOffset] = useState(0);

  const { data, isLoading, error } = useQuery({
    queryKey: ["employees", { limit: PAGE_SIZE, offset, search, country }],
    queryFn: () =>
      employeesApi.list({
        limit: PAGE_SIZE,
        offset,
        search: search || undefined,
        country: country || undefined,
      }),
    placeholderData: (prev) => prev,
  });

  const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 0;
  const currentPage = Math.floor(offset / PAGE_SIZE) + 1;

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-8 text-center">
        <p className="text-red-600">Failed to load employees. Is the backend running?</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Job Title</TableHead>
            <TableHead>Department</TableHead>
            <TableHead>Country</TableHead>
            <TableHead className="text-right">Salary</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Hire Date</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            <TableRow>
              <TableCell colSpan={8} className="text-center py-8 text-gray-500">
                Loading...
              </TableCell>
            </TableRow>
          ) : data?.data.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} className="text-center py-8 text-gray-500">
                No employees found
              </TableCell>
            </TableRow>
          ) : (
            data?.data.map((employee) => (
              <TableRow key={employee.id}>
                <TableCell className="font-medium">{employee.full_name}</TableCell>
                <TableCell>{employee.job_title}</TableCell>
                <TableCell>{employee.department || "—"}</TableCell>
                <TableCell>{employee.country}</TableCell>
                <TableCell className="text-right">
                  {formatSalary(employee.salary, employee.currency)}
                </TableCell>
                <TableCell>
                  <Badge variant="secondary">{employee.employment_type}</Badge>
                </TableCell>
                <TableCell>{formatDate(employee.hire_date)}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onEdit(employee)}
                      title="Edit"
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => onDelete(employee)}
                      title="Delete"
                    >
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      {/* Pagination */}
      {data && data.total > 0 && (
        <div className="flex items-center justify-between border-t px-4 py-3">
          <p className="text-sm text-gray-500">
            Showing {offset + 1}–{Math.min(offset + PAGE_SIZE, data.total)} of{" "}
            {data.total} employees
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={offset === 0}
              onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Previous
            </Button>
            <span className="text-sm text-gray-600">
              Page {currentPage} of {totalPages || 1}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={offset + PAGE_SIZE >= (data?.total || 0)}
              onClick={() => setOffset(offset + PAGE_SIZE)}
            >
              Next
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}