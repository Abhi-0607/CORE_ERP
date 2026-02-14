"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="rounded-xl bg-white p-8 shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center">Core ERP</h1>

        <div className="mt-6 flex flex-col gap-3">
          <button
            className="w-full rounded-lg bg-black px-4 py-2 text-white"
            onClick={() => router.push("/signup")}
          >
            Sign Up
          </button>

          <button
            className="w-full rounded-lg border px-4 py-2"
            onClick={() => router.push("/login")}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
}
