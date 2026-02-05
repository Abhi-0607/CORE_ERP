"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";
import { NAV_GROUPS, NAV_TOP, Role } from "@/config/navigation";

type Props = {
  role: Role;
};

export default function Sidebar({ role }: Props) {
  const pathname = usePathname();

  const [collapsed, setCollapsed] = useState(false);
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({});

  // restore sidebar scroll
  useEffect(() => {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    const savedScroll = localStorage.getItem("sidebarScroll");
    if (savedScroll) sidebar.scrollTop = Number(savedScroll);

    const onScroll = () => {
      localStorage.setItem("sidebarScroll", String(sidebar.scrollTop));
    };

    sidebar.addEventListener("scroll", onScroll);
    return () => sidebar.removeEventListener("scroll", onScroll);
  }, []);

  const topItems = useMemo(
    () => NAV_TOP.filter((x) => x.roles.includes(role)),
    [role]
  );

  const groups = useMemo(() => {
    return NAV_GROUPS.filter((g) => g.roles.includes(role)).map((g) => ({
      ...g,
      items: g.items.filter((i) => i.roles.includes(role)),
    }));
  }, [role]);

  function isActive(href: string) {
    if (href === "/dashboard" && pathname === "/dashboard") return true;
    return pathname.startsWith(href);
  }

  function toggleGroup(name: string) {
    setOpenGroups((prev) => ({ ...prev, [name]: !prev[name] }));
  }

  return (
    <aside
      id="sidebar"
      className={`h-[calc(100vh-0px)] sticky top-0 overflow-y-auto border-r bg-white transition-all duration-200 ${
        collapsed ? "w-20" : "w-72"
      }`}
    >
      {/* Collapse button */}
      <div className="flex items-center justify-between px-3 py-3 border-b">
        {!collapsed ? (
          <div className="text-sm font-semibold text-gray-800">
            Navigation
          </div>
        ) : (
          <div className="text-sm font-semibold text-gray-800"> </div>
        )}

        <button
          onClick={() => setCollapsed((v) => !v)}
          className="h-10 w-10 rounded-xl border bg-white hover:bg-gray-50 flex items-center justify-center"
          aria-label="collapse sidebar"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Top items */}
      <div className="p-2">
        {topItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-2xl px-3 py-3 text-sm transition ${
                active
                  ? "bg-black text-white"
                  : "text-gray-700 hover:bg-gray-50"
              }`}
            >
              <Icon size={18} />
              {!collapsed && <span className="font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </div>

      {/* Groups */}
      <div className="px-2 pb-4">
        {groups.map((group) => {
          const isOpen = openGroups[group.group] ?? true;
          const GroupIcon = group.icon;

          return (
            <div key={group.group} className="mb-2">
              <button
                onClick={() => toggleGroup(group.group)}
                className="w-full flex items-center justify-between rounded-2xl px-3 py-3 text-sm text-gray-800 hover:bg-gray-50"
              >
                <div className="flex items-center gap-3">
                  <GroupIcon size={18} />
                  {!collapsed && (
                    <span className="font-semibold">{group.group}</span>
                  )}
                </div>

                {!collapsed && (
                  <ChevronDown
                    size={18}
                    className={`transition ${isOpen ? "rotate-180" : ""}`}
                  />
                )}
              </button>

              {isOpen && !collapsed && (
                <div className="ml-4 mt-1 space-y-1 border-l pl-3">
                  {group.items.map((item) => {
                    const Icon = item.icon;
                    const active = isActive(item.href);

                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={`flex items-center gap-3 rounded-2xl px-3 py-2 text-sm transition ${
                          active
                            ? "bg-gray-100 text-black"
                            : "text-gray-700 hover:bg-gray-50"
                        }`}
                      >
                        <Icon size={16} />
                        <span>{item.label}</span>
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </aside>
  );
}
