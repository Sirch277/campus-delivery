"use client";
import { useState } from "react";
import { useEffect } from "react";
import api from "../../utils/api";
import Navbar from "../../components/Navbar";
import { useRouter } from "next/navigation";
import { getUserRole } from "../../utils/auth";


export default function NewDelivery() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [pickup, setPickup] = useState("");
  const [dropoff, setDropoff] = useState("");
  const [parcelType, setParcelType] = useState("");
  const [amount, setAmount] = useState(5); 
  const [authorized, setAuthorized] = useState(false);
  
  useEffect(() => {
  const role = getUserRole();
  if (role !== "customer") router.push("/");
  else setAuthorized(true);
}, [router]);
if (!authorized) return null;
  

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (amount < 5) {
      alert("Minimum delivery amount is 5 RMB");
      return;
    }
    try {
      await api.post("/api/delivery/", {
        title,
        description,
        pickup_location: pickup,
        dropoff_location: dropoff,
        parcel_type: parcelType,
        amount,
      });
      alert("Delivery created successfully!");
      router.push("/customer/my-deliveries");
    } catch (err: any) {
      alert("Failed to create delivery");
      console.error(err);
    }
  }

  return (
    <>
      <Navbar />
      <div className="max-w-md mx-auto mt-10 p-4 border rounded-lg shadow-md bg-white">
        <h1 className="text-2xl font-bold mb-4">New Delivery Request</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border p-2"
            required
          />
          <textarea
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="border p-2"
          />
          <input
            placeholder="Pickup location"
            value={pickup}
            onChange={(e) => setPickup(e.target.value)}
            className="border p-2"
            required
          />
          <input
            placeholder="Dropoff location"
            value={dropoff}
            onChange={(e) => setDropoff(e.target.value)}
            className="border p-2"
            required
          />
          <input
            placeholder="Parcel Type (e.g., Food, Documents, Electronics)"
            value={parcelType}
            onChange={(e) => setParcelType(e.target.value)}
            className="border p-2"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Delivery Fee (min 5 RMB)
            </label>
            <input
              type="number"
              min={5}
              step="0.5"
              value={amount}
              onChange={(e) => setAmount(parseFloat(e.target.value))}
              className="border p-2 w-full"
              required
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
          >
            Create Delivery
          </button>
        </form>
      </div>
    </>
  );
}
