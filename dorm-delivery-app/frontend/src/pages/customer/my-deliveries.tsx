"use client";
import useSWR from "swr";
import api from "../../utils/api";
import Navbar from "../../components/Navbar";
import { getUserRole } from "../../utils/auth";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useState } from "react";
const fetcher = (url: string) => api.get(url).then(res => res.data);


    
export default function MyDeliveries() {
  const { data: deliveries, error } = useSWR("/api/delivery/", fetcher);
  const [authorized, setAuthorized] = useState(false);
  const router = useRouter();
    
useEffect(() => {
    const role = getUserRole();

    
    if (role !== "customer") router.push("/");
    else setAuthorized(true);
},  [router]);
  if (!authorized) return null;

  if (error) return <p>Error loading deliveries.</p>;
  if (!deliveries) return <p>Loading...</p>;

  return (
    <>
      <Navbar />
      <div className="p-4 grid gap-4">
        {deliveries.map((d: any) => (
  <div
    key={d.id}
    className="border p-4 rounded-md shadow-sm bg-white flex flex-col gap-1"
  >
    <h2 className="text-xl font-bold">{d.title}</h2>
    <p className="text-gray-600">{d.description}</p>
    <p>Status: <strong>{d.status}</strong></p>
    <p>Pickup: {d.pickup_location}</p>
    <p>Dropoff: {d.dropoff_location}</p>

    {d.status === "delivered" && (
      <button
        onClick={async () => {
          try {
            await api.post(`/api/delivery/${d.id}/confirm`);
            alert("Delivery confirmed");
            location.reload(); // simple refresh after update
          } catch (err) {
            alert("Failed to confirm delivery");
          }
        }}
        className="bg-green-600 text-white mt-2 px-3 py-1 rounded hover:bg-green-700"
      >
        Confirm Delivery
      </button>
    )}
  </div>
))}

      </div>
    </>
  );
}
