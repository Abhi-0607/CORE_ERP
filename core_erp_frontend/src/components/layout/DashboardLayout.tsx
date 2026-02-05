"use client";

import { useRouter } from "next/navigation";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import { Role } from "@/config/navigation";

type Props = {
  children: React.ReactNode;
};

export default function DashboardLayout({ children }: Props) {
  const router = useRouter();

  /**
   * TEMP DUMMY USER
   * Later: read token from localStorage and decode role
   */
  const user = {
    full_name: "Abhignya Gitti",
    role: "ADMIN" as Role,
  };

  function logout() {
    localStorage.removeItem("access_token");
    router.push("/login");
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        <Sidebar role={user.role} />

        <div className="flex-1">
          <Topbar userName={user.full_name} role={user.role} onLogout={logout} />

          <main className="p-5">
            <div className="rounded-2xl border bg-white p-5 shadow-sm">
              {children}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
