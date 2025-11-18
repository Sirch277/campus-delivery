"use client";
import useSWR, { mutate } from "swr";
import api from "../../utils/api";
import Navbar from "../../components/Navbar";
import OrderCard from "../../components/OrderCard";
import { useRouter } from "next/router"; 
import { useState } from "react";
import { useEffect } from "react";
import { getUserRole } from "src/utils/auth";
const fetcher = (url: string) => api.get(url).then((res) => res.data);

export default function AvailableTasks() {
  const { data: tasks, error } = useSWR("/api/delivery/available-tasks", fetcher);
  const router = useRouter();


  const [authorized, setAuthorized] = useState(false);
      
  useEffect(() => {
      const role = getUserRole();
  
      
      if (role !== "delivery") router.push("/");
      else setAuthorized(true);
  },  [router]);
    if (!authorized) return null;
    if (error) return <p>Error loading available tasks.</p>;
    if (!tasks) return <p>Loading...</p>;
   async function handleAccept(taskId: number) {
    console.log("Accepting taskId:", taskId);
    try {
      await api.post(`/api/delivery/${taskId}/accept`);
      alert("Task accepted!");
      router.push("/delivery/my-tasks");
    } catch (err) {
      console.error(err);
      alert("Failed to accept task");
    }
  }

   return (
    <>
      <Navbar />
      <div className="p-4 grid gap-4">
        {tasks.map((task: any) => (
          <div
            key={task.id}
            className="border p-3 rounded-md shadow-sm bg-white flex flex-col"
          >
            <OrderCard order={task} onAccept={() => handleAccept(task.id)} />
          </div>
        ))}
      </div>
    </>
  );
}