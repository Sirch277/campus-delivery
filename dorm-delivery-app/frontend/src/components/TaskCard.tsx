type Task = {
  id: number;
  order_id: number;
  customer_name: string;
  address: string;
  status: string;
};

export default function TaskCard({ task, onAccept }: { task: Task; onAccept?: () => void }) {
  return (
    <div className="border p-3 rounded-md bg-white shadow-sm flex justify-between items-center">
      <div>
        <p><strong>Order #{task.order_id}</strong></p>
        <p>{task.customer_name}</p>
        <p>{task.address}</p>
        <p>Status: {task.status}</p>
      </div>
      {onAccept && (
        <button
          onClick={onAccept}
          className="bg-green-500 text-white px-3 py-1 rounded-md"
        >
          Accept
        </button>
      )}
    </div>
  );
}
