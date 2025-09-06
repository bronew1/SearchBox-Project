"use client";

import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
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
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <img
          src="/sinagif.gif" // public klasöründe olmalı
          alt="Yükleniyor..."
          className="w-32 h-32"
        />
      </div>
    );
  }

  return (
    <div>
      {/* Kartlar */}
      <div className="flex flex-wrap gap-6 mb-8">
        <div className="bg-white shadow rounded-xl p-6 w-60 border border-gray-100">
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

        <div className="bg-white shadow rounded-xl p-6 w-60 border border-gray-100">
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

        <div className="bg-white shadow rounded-xl p-6 flex-1 min-w-[250px] border border-pink-200">
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

      {/* Tarih aralığı */}
      <div className="flex items-center gap-4 mb-4">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border rounded-lg p-2 shadow-sm"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border rounded-lg p-2 shadow-sm"
        />
        <button
          onClick={handleApplyFilters}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg shadow-md transition"
        >
          Uygula
        </button>
      </div>

      {/* Grafik */}
      <div className="bg-white rounded-xl p-6 shadow border border-gray-100">
        <h2 className="text-lg font-bold mb-4 text-gray-800">
          En Çok Görüntülenen Ürünler
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={products} barSize={45}>
            {/* ✅ Grid kaldırıldı */}
            <XAxis
              dataKey="short_id"
              angle={-30}
              textAnchor="end"
              interval={0}
              height={60}
              tick={{ fill: "#6b7280", fontSize: 12 }}
            />
            <YAxis hide />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid #e5e7eb",
                borderRadius: "0.75rem",
                boxShadow: "0 6px 12px rgba(0,0,0,0.08)",
              }}
              formatter={(value: number, name: string, props: any) => [
                `${value} görüntülenme`,
                props.payload.product_id,
              ]}
              cursor={{ fill: "rgba(0,0,0,0.03)" }}
            />

            {/* ✅ Gradient */}
            <defs>
              <linearGradient id="pinkGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#ec4899" stopOpacity={0.9} />
                <stop offset="100%" stopColor="#fbcfe8" stopOpacity={0.7} />
              </linearGradient>
            </defs>

            <Bar dataKey="count" fill="url(#pinkGradient)" radius={[10, 10, 0, 0]}>
              <LabelList
                dataKey="count"
                position="top"
                fill="#374151"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
