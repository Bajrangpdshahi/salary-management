"use client";

import { useState, useCallback } from "react";
import { EmployeeSearch } from "@/components/employees/EmployeeSearch";
import { EmployeeTable } from "@/components/employees/EmployeeTable";
import { EmployeeForm } from "@/components/employees/EmployeeForm";
import { DeleteConfirmDialog } from "@/components/employees/DeleteConfirmDialog";
import { Button } from "@/components/ui/button";
import type { Employee } from "@/types/employee";
import { Plus } from "lucide-react";

export default function EmployeesPage() {
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deletingEmployee, setDeletingEmployee] = useState<Employee | null>(null);

  const handleEdit = useCallback((employee: Employee) => {
    setEditingEmployee(employee);
    setFormOpen(true);
  }, []);

  const handleDelete = useCallback((employee: Employee) => {
    setDeletingEmployee(employee);
    setDeleteOpen(true);
  }, []);

  const handleAdd = useCallback(() => {
    setEditingEmployee(null);
    setFormOpen(true);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Employees</h1>
        <Button onClick={handleAdd}>
          <Plus className="h-4 w-4 mr-2" />
          Add Employee
        </Button>
      </div>

      <EmployeeSearch
        search={search}
        onSearchChange={setSearch}
        country={country}
        onCountryChange={setCountry}
      />

      <EmployeeTable
        search={search}
        country={country}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <EmployeeForm
        open={formOpen}
        onOpenChange={setFormOpen}
        employee={editingEmployee}
      />

      <DeleteConfirmDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        employee={deletingEmployee}
      />
    </div>
  );
}