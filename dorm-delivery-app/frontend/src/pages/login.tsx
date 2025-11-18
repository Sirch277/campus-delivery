"use client";
import { useState, useEffect } from "react";
import { loginUser } from "../utils/auth";
import { useRouter } from "next/navigation";
import Navbar from "../components/Navbar";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();


  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      await loginUser({ email, password });
      const role = localStorage.getItem("role");
      if (role === "delivery") router.push("/delivery/available-tasks");
      else router.push("/customer/my-deliveries");



    } catch (err) {
      alert("Invalid credentials");
      
    }
  }
  useEffect(() => {
    try {
      const token = localStorage.getItem("token");
      if (!token) return;
      const payload = JSON.parse(atob(token.split(".")[1]));
      const role = payload?.role;
      if (role === "customer") router.push("/customer/my-orders");
      else if (role === "delivery") router.push("/delivery/available-tasks");
    } catch (err) {
      // ignore invalid token
    }
  }, [router]);


  return (
    <>
      <Navbar />
      <form
        onSubmit={handleSubmit}
        className="max-w-sm mx-auto mt-10 flex flex-col gap-3"
      >
        <input
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2"
        />
        <button className="bg-blue-600 text-white p-2 rounded-md">
          Login
        </button>
      </form>
    </>
  );
}
