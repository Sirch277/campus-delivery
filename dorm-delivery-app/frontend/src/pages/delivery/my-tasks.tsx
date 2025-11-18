"use client";
import useSWR from "swr";
import api from "../../utils/api";
import Navbar from "../../components/Navbar";
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/router"; 
import { getUserRole } from "src/utils/auth";


const fetcher = (url: string) => api.get(url).then((res) => res.data);

export default function MyTasks() {
  const { data: tasks, error, mutate } = useSWR("/api/delivery/my", fetcher);



  const [authorized, setAuthorized] = useState(false);
  const router = useRouter();
      
  useEffect(() => {
      const role = getUserRole();
  
      
      if (role !== "delivery") router.push("/");
      else setAuthorized(true);
  },  [router]);
      if (!authorized) return null;
      if (error) return <p>Error loading assigned tasks.</p>;
      if (!tasks) return <p>Loading...</p>;

  async function updateStatus(taskId: number, action: string) {
    try {
      await api.post(`/api/delivery/${taskId}/${action}`);
      mutate(); // refresh tasks
    } catch (err) {
      console.error(err);
      alert("Failed to update task status");
    }
  }

  return (
    <>
      <Navbar />
      <div className="p-4 grid gap-4">
        {tasks.map((task: any) => (
          <div key={task.id} className="border p-3 rounded bg-white">
            <p><b>{task.title}</b></p>
            <p>Pickup: {task.pickup_location}</p>
            <p>Dropoff: {task.dropoff_location}</p>
            <p>Description: {task.description}</p>
            <p>Status: {task.status}</p>
            {task.status === "accepted" && (
              <button
                className="bg-blue-500 text-white px-3 py-1 rounded"
                onClick={() => updateStatus(task.id, "start")}
              >
                Start Delivery
              </button>
            )}
            {task.status === "in_progress" && (
              <button
                className="bg-green-500 text-white px-3 py-1 rounded"
                onClick={() => updateStatus(task.id, "mark-delivered")}
              >
                Mark Delivered
              </button>
            )}
            {task.status === "delivered" && (
              <p>Waiting for customer confirmation...</p>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
