"use client";

import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import API from "@/services/api";
import type { Role } from "@/config/navigation";

type MeResponse = {
  id: number;
  email: string;
  role: Role;
  full_name?: string | null;
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [me, setMe] = useState<MeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMe = async () => {
      try {
        const res = await API.get("/auth/me");
        setMe(res.data);
      } catch (err) {
        setMe(null);
      } finally {
        setLoading(false);
      }
    };

    loadMe();
  }, []);

  // while loading, show a simple skeleton
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-sm text-gray-600">
        Loading...
      </div>
    );
  }

  // If token missing / invalid
  if (!me) {
    return (
      <div className="min-h-screen flex items-center justify-center text-sm text-red-600">
        Unauthorized. Please login again.
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-72 border-r bg-white">
        <Sidebar role={me.role} />
      </div>

      {/* Main */}
      <div className="flex-1 flex flex-col">
        <Topbar user={me} />

        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
