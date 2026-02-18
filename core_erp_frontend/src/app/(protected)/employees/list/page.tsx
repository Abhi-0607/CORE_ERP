"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import API from "@/services/api";

type Employee = {
  id: number;

  first_name: string;
  last_name: string;

  employee_id: string;

  department?: string | null;

  date_of_joining?: string | null;

  reporting_to?: number | null;

  invite_sent: boolean;
  invite_sent_at?: string | null;
};

type EmployeeListResponse = {
  employees: Employee[];
  total: number;
  page: number;
  per_page: number;
};

export default function EmployeesListPage() {
  const router = useRouter();

  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [sendingInviteId, setSendingInviteId] = useState<number | null>(null);

  const fetchEmployees = async () => {
    try {
      setLoading(true);

      const res = await API.get<EmployeeListResponse>("/employees", {
        params: {
          skip: 0,
          limit: 100,
        },
      });

      setEmployees(res.data.employees || []);
    } catch (err: any) {
      console.error("Failed to fetch employees:", err);

      if (err?.response?.status === 401) {
        router.push("/login");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleSendInvite = async (employeeId: number) => {
    try {
      setSendingInviteId(employeeId);

      await API.post(`/employees/${employeeId}/send-invite`);

      // refresh so button disappears
      await fetchEmployees();
    } catch (err: any) {
      console.error("Invite error:", err);
      alert(err?.response?.data?.detail || "Failed to send invite");
    } finally {
      setSendingInviteId(null);
    }
  };

  // ✅ LIFO (latest employee on top)
  const rows = useMemo(() => {
    return [...employees].reverse();
  }, [employees]);

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-2xl font-semibold">Employees</h1>

        <button
          onClick={() => router.push("/employees/register")}
          className="px-4 py-2 rounded bg-black text-white hover:opacity-90"
        >
          + Add Employee
        </button>
      </div>

      {loading ? (
        <div className="text-gray-600">Loading employees...</div>
      ) : rows.length === 0 ? (
        <div className="text-gray-600">No employees found.</div>
      ) : (
        <div className="overflow-x-auto border rounded">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 text-left">
              <tr>
                <th className="p-3">S. No</th>
                <th className="p-3">Employee Name</th>
                <th className="p-3">Employee ID</th>
                <th className="p-3">Department</th>
                <th className="p-3">Date of Joining</th>
                <th className="p-3">Reporting To</th>
                <th className="p-3">Actions</th>
              </tr>
            </thead>

            <tbody>
              {rows.map((emp, index) => (
                <tr key={emp.id} className="border-t">
                  {/* ✅ inverted S.No */}
                  <td className="p-3 font-medium">
                    {rows.length - index}
                  </td>

                  <td className="p-3">
                    {emp.first_name} {emp.last_name}
                  </td>

                  <td className="p-3">{emp.employee_id}</td>

                  <td className="p-3">{emp.department || "-"}</td>

                  <td className="p-3">{emp.date_of_joining || "-"}</td>

                  <td className="p-3">
                    {emp.reporting_to ? emp.reporting_to : "-"}
                  </td>

                  <td className="p-3">
                    {!emp.invite_sent ? (
                      <button
                        onClick={() => handleSendInvite(emp.id)}
                        disabled={sendingInviteId === emp.id}
                        className="px-3 py-1 rounded bg-red-600 text-white hover:opacity-90 disabled:opacity-50"
                      >
                        {sendingInviteId === emp.id
                          ? "Sending..."
                          : "Send Invite"}
                      </button>
                    ) : (
                      <span className="text-green-700 font-medium">
                        Sent ✅
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
