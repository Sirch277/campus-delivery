"use client";
import { useEffect, useState } from "react";
import { getUserRole, isLoggedIn, logout } from "../utils/auth";

export default function Navbar() {
  const [role, setRole] = useState<string | null>(null);
  const [loggedIn, setLoggedIn] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setRole(getUserRole());
    setLoggedIn(isLoggedIn());
    setHydrated(true); // client has hydrated
  }, []);

  if (!hydrated) return null; // avoid server/client mismatch

  return (
    <nav className="flex justify-between p-4 bg-gray-200">
      <a href="/">Dorm Delivery</a>

      <div className="flex gap-4 items-center">
        {/* When not logged in */}
        {!loggedIn && (
          <>
            <a href="/register">Register</a>
            <a href="/login">Login</a>
          </>
        )}

        {/* Customer Links */}
        {role === "customer" && (
          <>
            <a href="/customer/my-deliveries">My Requests</a>
            <a href="/customer/new-delivery">New Delivery</a>
          </>
        )}

        {/* Delivery Links */}
        {role === "delivery" && (
          <>
            <a href="/delivery/available-tasks">Available Tasks</a>
            <a href="/delivery/my-tasks">My Tasks</a>
          </>
        )}

        {/* 👇 Admin Link */}
        {role === "admin" && (
          <a
            href="/admin/dashboard"
            className="text-blue-600 font-semibold hover:underline"
          >
            Admin Dashboard
          </a>
        )}

        {/* Logout Button */}
        {loggedIn && (
          <button
            onClick={logout}
            className="bg-red-500 text-white px-3 py-1 rounded"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
