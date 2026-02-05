"use client";

import { useEffect, useRef, useState } from "react";
import { LogOut, Settings, User } from "lucide-react";

type Props = {
  userName: string;
  role: string;
  onLogout?: () => void;
};

export default function Topbar({ userName, role, onLogout }: Props) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (!menuRef.current) return;
      if (!menuRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  return (
    <div className="sticky top-0 z-40 w-full border-b bg-white">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Left */}
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-black text-white flex items-center justify-center font-bold">
            C
          </div>
          <div>
            <div className="text-sm font-semibold leading-tight">CORE ERP</div>
            <div className="text-xs text-gray-500 leading-tight">
              Admin Panel
            </div>
          </div>
        </div>

        {/* Right */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-sm font-semibold">{userName}</div>
            <div className="text-xs text-gray-500">{role}</div>
          </div>

          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setOpen((v) => !v)}
              className="h-10 w-10 rounded-xl border bg-white hover:bg-gray-50 flex items-center justify-center"
              aria-label="menu"
            >
              ⋮
            </button>

            {open && (
              <div className="absolute right-0 mt-2 w-52 overflow-hidden rounded-2xl border bg-white shadow-lg">
                <button className="w-full flex items-center gap-2 px-4 py-3 hover:bg-gray-50 text-sm">
                  <User size={18} />
                  My Profile
                </button>
                <button className="w-full flex items-center gap-2 px-4 py-3 hover:bg-gray-50 text-sm">
                  <Settings size={18} />
                  Settings
                </button>

                <div className="h-px bg-gray-100" />

                <button
                  onClick={onLogout}
                  className="w-full flex items-center gap-2 px-4 py-3 hover:bg-red-50 text-sm text-red-600"
                >
                  <LogOut size={18} />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
