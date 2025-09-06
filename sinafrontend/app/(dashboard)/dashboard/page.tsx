"use client";

import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type Stat = {
  count: number;
  change: number;
};

type DashboardStats = {
  total_events: Stat;
  add_to_cart: Stat;
};

type ProductData = {
  product_id: string;
  count: number;
  short_id?: string;
};

export default function DashboardStatsPanel() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [products, setProducts] = useState<ProductData[]>([]);
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [revenue, setRevenue] = useState<number | null>(null);

  useEffect(() => {
    const today = new Date();
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(today.getDate() - 7);

    const end = today.toISOString().split("T")[0];
    const start = sevenDaysAgo.toISOString().split("T")[0];

    setStartDate(start);
    setEndDate(end);

    fetchInitialStats();
    fetchRevenue(start, end);
    fetchProducts(start, end);
  }, []);

  const fetchInitialStats = () => {
    fetch("https://searchprojectdemo.com/api/dashboard-stats/")
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error(err));
  };

  const fetchProducts = (start?: string, end?: string) => {
    let url = "https://searchprojectdemo.com/api/most-viewed-products/";
    if (start && end) {
      url += `?start_date=${start}&end_date=${end}`;
    }
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const shortened = data.map((item: ProductData) => ({
          ...item,
          short_id:
            item.product_id.length > 7
              ? item.product_id.slice(0, 7) + "..."
              : item.product_id,
        }));
        setProducts(shortened);
      })
      .catch((err) => console.error(err));
  };

  const fetchRevenue = (start?: string, end?: string) => {
    let url = "https://searchprojectdemo.com/api/revenue/";
    if (start && end) {
      url += `?start_date=${start}&end_date=${end}`;
    }
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          setRevenue(data.revenue);
        }
      })
      .catch((err) => console.error(err));
  };

  const handleApplyFilters = () => {
    if (startDate && endDate) {
      fetchProducts(startDate, endDate);
      fetchRevenue(startDate, endDate);
    }
  };

  // ✅ Loading ekranı GIF ile
  if (!stats) {
    return (
      <div className="flex items-center justify-center h-screen">
        <img
          src="/sinagif.gif" // public klasörüne atılacak
          alt="Yükleniyor..."
          className="w-24 h-24"
        />
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-wrap gap-6 mb-8">
        {/* Kullanıcı Hareketleri */}
        <div className="bg-white shadow rounded p-6 w-60">
          <div className="text-gray-500 text-sm">Kullanıcı Hareketleri</div>
          <div className="text-2xl font-bold">
            {stats.total_events.count.toLocaleString()}
          </div>
          <div
            className={`text-sm mt-1 ${
              stats.total_events.change >= 0 ? "text-green-600" : "text-red-600"
            }`}
          >
            {stats.total_events.change >= 0 ? "▲" : "▼"}{" "}
            {Math.abs(stats.total_events.change)}%
          </div>
        </div>

        {/* Sepete Ekleme */}
        <div className="bg-white shadow rounded p-6 w-60">
          <div className="text-gray-500 text-sm">Sepete Ekleme</div>
          <div className="text-2xl font-bold">
            {stats.add_to_cart.count.toLocaleString()}
          </div>
          <div
            className={`text-sm mt-1 ${
              stats.add_to_cart.change >= 0 ? "text-green-600" : "text-red-600"
            }`}
          >
            {stats.add_to_cart.change >= 0 ? "▲" : "▼"}{" "}
            {Math.abs(stats.add_to_cart.change)}%
          </div>
        </div>

        {/* Ciro */}
        <div className="bg-white shadow rounded p-6 flex-1 min-w-[250px] border border-pink-200">
          <div className="text-gray-500 text-sm">Ciro</div>
          <div className="text-3xl font-bold text-pink-600">
            {revenue !== null
              ? revenue.toLocaleString("tr-TR", {
                  style: "currency",
                  currency: "TRY",
                })
              : "Yükleniyor..."}
          </div>
          <div className="text-xs text-gray-500 mt-1">
            {startDate && endDate ? `${startDate} - ${endDate}` : "Tüm Zamanlar"}
          </div>
        </div>
      </div>

      {/* Tarih aralığı seçimi */}
      <div className="flex items-center gap-4 mb-4">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border rounded p-2"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border rounded p-2"
        />
        <button
          onClick={handleApplyFilters}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded"
        >
          Uygula
        </button>
      </div>

      {/* Grafik */}
      <div className="bg-white rounded p-4 shadow">
        <h2 className="text-lg font-bold mb-4">En Çok Görüntülenen Ürünler</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={products}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="short_id"
              angle={-30}
              textAnchor="end"
              interval={0}
              height={60}
            />
            <YAxis />
            <Tooltip
              formatter={(value: number, name: string, props: any) => [
                `${value} görüntülenme`,
                props.payload.product_id,
              ]}
              cursor={{ fill: "rgba(0, 0, 0, 0.05)" }}
            />
            <Bar dataKey="count" fill="#ebbecb" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
