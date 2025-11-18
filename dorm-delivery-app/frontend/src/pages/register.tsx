"use client";
import { useState } from "react";
import { registerUser } from "../utils/auth";
import { useRouter } from "next/navigation";
import Navbar from "../components/Navbar";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("customer"); // default role
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      await registerUser({ username, email, password, role});
      alert("Registration successful! Please log in.");
      router.push("/login");
    } catch (err) {
      alert("Failed to register");
    }
  }

  return (
    <>
      <Navbar />
      <form
        onSubmit={handleSubmit}
        className="max-w-sm mx-auto mt-10 flex flex-col gap-3"
      >
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2"
        />
        <input
          placeholder="Email"
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

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="border p-2"
        >
          <option value="customer">Customer</option>
          <option value="delivery">Delivery</option>
        </select>

        <button className="bg-green-600 text-white p-2 rounded-md">
          Register
        </button>
      </form>
    </>
  );
}
