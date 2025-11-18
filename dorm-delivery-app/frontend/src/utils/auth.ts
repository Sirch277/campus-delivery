import api from "./api";
import { jwtDecode } from "jwt-decode";

const TOKEN_KEY = "access_token";

export async function registerUser(payload: { username: string; email: string; password: string; role: string }) {
  const res = await api.post("/api/auth/register", payload);
  return res.data;
}

export async function loginUser(payload: { email: string; password: string }) {
  const res = await api.post("/api/auth/login", payload);
  const token = res.data?.access_token;

  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    // decode and store role
    try {
      const decoded: any = jwtDecode(token);
      if (decoded?.role) {
        localStorage.setItem("role", decoded.role);
      }
    } catch (err) {
      console.error("Error decoding JWT:", err);
    }
  }

  return res.data;
}

export function logoutUser() {
  localStorage.removeItem(TOKEN_KEY);
  delete api.defaults.headers.common["Authorization"];
}

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function isLoggedIn() {
  if (typeof window === "undefined") return false;
  return !!getToken();
}

// set token on initial load (use inside client components)
export function hydrateToken() {
  if (typeof window === "undefined") return;
  const t = getToken();
  if (t) api.defaults.headers.common["Authorization"] = `Bearer ${t}`;
}

export function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "/"; // redirect to home
}

export function getUserRole() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;
  try {
    const decoded: any = jwtDecode(token);
    return decoded.role;
  } catch {
    return null;
  }
}

import { useState, useEffect } from "react";

export function useIsLoggedIn() {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setLoggedIn(!!token);
  }, []);

  return loggedIn;


  
}

