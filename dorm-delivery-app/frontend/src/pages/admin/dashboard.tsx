"use client";
import useSWR from "swr";
import api from "../../utils/api";
import Navbar from "../../components/Navbar";
import { useEffect, useState } from "react";
import { getUserRole } from "../../utils/auth";

const fetcher = (url: string) => api.get(url).then((res) => res.data);

export default function Dashboard() {
  const { data, error } = useSWR("/api/admin/stats", fetcher);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const role = getUserRole();
    if (role === "admin") setIsAdmin(true);
  }, []);

  if (!isAdmin) return <p>You are not authorized to view this page.</p>;
  if (error) return <p>Failed to load dashboard</p>;
  if (!data) return <p>Loading...</p>;

  return (
    <>
      <Navbar />
      <div className="p-6 space-y-4">
        <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">Total Users</div>
            <div className="text-2xl font-semibold">{data.users_count}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">Total Deliveries</div>
            <div className="text-2xl font-semibold">{data.total_deliveries}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">Active Deliveries</div>
            <div className="text-2xl font-semibold">{data.active_deliveries}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">Pending Deliveries</div>
            <div className="text-2xl font-semibold">{data.pending_deliveries}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">In Progress</div>
            <div className="text-2xl font-semibold">{data.in_progress}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <div className="text-gray-500">Held Payments</div>
            <div className="text-2xl font-semibold">{data.total_held_payments}</div>
          </div>
        </div>
      </div>
    </>
  );
}
