type Order = {
  id: number;
  title: string;
  status: string;
  description: string;
};

export default function OrderCard({ order, onAccept }: { order: any, onAccept?: () => void }) {
  return (
    <div className="border p-3 rounded-md shadow-sm bg-white">
      <h3 className="font-semibold">{order.title}</h3>
      <p>description: {order.description}</p>
      <p>Status: {order.status}</p>
      {onAccept && (
        <button
          onClick={onAccept}
          className="bg-green-500 text-white px-3 py-1 mt-2 rounded-md"
        >
          Accept
        </button>
      )}
      
      


    </div>
  );
}
