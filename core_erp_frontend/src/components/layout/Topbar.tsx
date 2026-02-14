"use client";

export default function Topbar({
  user,
}: {
  user: { full_name?: string | null; email: string; role: string };
}) {
  return (
    <div className="h-16 border-b bg-white px-6 flex items-center justify-between">
      <div>
        <div className="text-sm font-semibold text-gray-900">
          {user.full_name || user.email}
        </div>
        <div className="text-xs text-gray-600">{user.role}</div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={() => {
            localStorage.removeItem("access_token");
            window.location.href = "/login";
          }}
          className="rounded-2xl border px-4 py-2 text-sm hover:bg-gray-50"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
