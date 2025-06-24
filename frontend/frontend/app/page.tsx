// app/page.tsx
"use client";

import { useEffect, useState } from "react";
import Sidebar from "./AppSidebar";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface Stat {
  day: string;
  count: number;
}

export default function Home() {
  const [data, setData] = useState<Stat[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/daily-add-to-cart-stats/")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Veri alınamadı:", err));
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6">
        <h2 className="text-xl font-bold mb-4">📈 Günlük Sepete Ekleme İstatistikleri</h2>
        <div className="bg-white p-4 rounded-lg shadow">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
