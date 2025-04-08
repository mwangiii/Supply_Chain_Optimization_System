import React, { useEffect, useState } from "react";

interface Eta {
  estimatedTime: string;
  [key: string]: unknown;
}

interface Order {
  id: string;
  status: string;
  [key: string]: unknown;
}

interface Delay {
  id: string;
  reason: string;
  [key: string]: unknown;
}

interface OrderResponse {
  message: string;
  status: string;
  data: Order[] | null;
  errors: { message: string; code?: string }[];
}

interface SingleOrderResponse {
  message: string;
  status: string;
  data: Order | null;
  errors: { message: string; code?: string }[];
}

interface DelayResponse {
  message: string;
  status: string;
  data: Delay[] | null;
  errors: { message: string; code?: string }[];
}

interface EtaResponse {
  message: string;
  status: string;
  data: Eta | null;
  errors: { message: string; code?: string }[];
}

const Tracking: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [order, setOrder] = useState<Order | null>(null);
  const [delays, setDelays] = useState<Delay[]>([]);
  const [eta, setEta] = useState<Eta | null>(null);
  const [orderId, setOrderId] = useState("");

  const baseUrl = import.meta.env.VITE_BASE_API_URL;

  useEffect(() => {
    fetch(`${baseUrl}/tracking/orders`)
      .then((res) => res.json())
      .then((data: OrderResponse) => {
        if (Array.isArray(data.data)) {
          setOrders(data.data);
        } else {
          setOrders([]);
        }
      });

    fetch(`${baseUrl}/tracking/delays`)
      .then((res) => res.json())
      .then((data: DelayResponse) => {
        if (Array.isArray(data.data)) {
          setDelays(data.data);
        } else {
          setDelays([]);
        }
      });

    fetch(`${baseUrl}/tracking/eta`)
      .then((res) => res.json())
      .then((data: EtaResponse) => {
        if (data.data && typeof data.data === "object") {
          setEta(data.data);
        } else {
          setEta(null);
        }
      });
  }, []);

  const handleFetchOrder = () => {
    fetch(`${baseUrl}/tracking/order/${orderId}`)
      .then((res) => res.json())
      .then((data: SingleOrderResponse) => {
        if (data.data && typeof data.data === "object") {
          setOrder(data.data);
        } else {
          setOrder(null);
        }
      });
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">Tracking Dashboard</h1>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">All Orders</h2>
        <div className="bg-white shadow rounded-xl p-4">
          <pre className="text-sm overflow-x-auto">{JSON.stringify(orders, null, 2)}</pre>
        </div>
      </div>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Get Order by ID</h2>
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Enter order ID"
            value={orderId}
            onChange={(e) => setOrderId(e.target.value)}
            className="border px-4 py-2 rounded w-full max-w-sm"
          />
          <button
            onClick={handleFetchOrder}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Fetch
          </button>
        </div>
        {order && (
          <div className="bg-white shadow rounded-xl p-4 mt-4">
            <pre className="text-sm overflow-x-auto">{JSON.stringify(order, null, 2)}</pre>
          </div>
        )}
      </div>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Delays</h2>
        <div className="bg-white shadow rounded-xl p-4">
          <pre className="text-sm overflow-x-auto">{JSON.stringify(delays, null, 2)}</pre>
        </div>
      </div>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">ETA</h2>
        <div className="bg-white shadow rounded-xl p-4">
          <pre className="text-sm overflow-x-auto">{JSON.stringify(eta, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
};

export default Tracking;
