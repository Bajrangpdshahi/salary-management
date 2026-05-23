"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { employeesApi } from "@/lib/api";
import { useDebounce } from "@/lib/hooks";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface EmployeeSearchProps {
  search: string;
  onSearchChange: (value: string) => void;
  country: string;
  onCountryChange: (value: string) => void;
}

export function EmployeeSearch({
  search,
  onSearchChange,
  country,
  onCountryChange,
}: EmployeeSearchProps) {
  const [localSearch, setLocalSearch] = React.useState(search);
  const debouncedSearch = useDebounce(localSearch, 300);

  React.useEffect(() => {
    onSearchChange(debouncedSearch);
  }, [debouncedSearch, onSearchChange]);

  const { data: paginated } = useQuery({
    queryKey: ["employees", { limit: 200, offset: 0 }],
    queryFn: () => employeesApi.list({ limit: 200, offset: 0 }),
  });

  const countries = React.useMemo(() => {
    if (!paginated?.data) return [];
    const set = new Set(paginated.data.map((e) => e.country));
    return Array.from(set).sort();
  }, [paginated]);

  return (
    <div className="flex gap-3">
      <Input
        placeholder="Search by name or job title..."
        value={localSearch}
        onChange={(e) => setLocalSearch(e.target.value)}
        className="max-w-sm"
      />
      <Select value={country} onValueChange={onCountryChange}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="All Countries" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">All Countries</SelectItem>
          {countries.map((c) => (
            <SelectItem key={c} value={c}>
              {c}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}