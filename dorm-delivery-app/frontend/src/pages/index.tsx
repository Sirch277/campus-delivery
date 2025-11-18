"use client";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useEffect, useState } from "react";
import api from "../utils/api";
import Link from "next/link"; // 👈 for navigation

export default function Home() {
  const [msg, setMsg] = useState("");
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    api.get("/").then((res) => setMsg(res.data.msg)).catch(console.error);

    // get role from localStorage
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);
  }, []);

  return (
    <>
      <Navbar />
      <main className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-3xl font-bold">Welcome to Dorm Delivery</h1>
        <p className="text-gray-600">Order anything. Get it delivered fast.</p>

        <h1 className="text-2xl font-bold">Backend says:</h1>
        <p>{msg}</p>

        
        {role === "admin" && (
          <Link
            href="/admin"
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Go to Admin Dashboard
          </Link>
        )}
      </main>
      <Footer />
    </>
  );
}
