"use client";
import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { ShoppingCart } from "lucide-react";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default function DashboardPage() {
  const [data, setData] = useState<any[]>([]);
  const [startDate, setStartDate] = useState("2025-06-04");
  const [endDate, setEndDate] = useState("2025-07-03");

  const fetchData = () => {
    fetch(`https://searchprojectdemo.com/api/daily-add-to-cart/?start_date=${startDate}&end_date=${endDate}`)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("API error:", err));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const chartData = {
    labels: data.map((item) => item.day),
    datasets: [
      {
        label: "Sepete Eklemeler",
        data: data.map((item) => item.count),
        fill: true,
        backgroundColor: "rgba(236, 72, 153, 0.15)", // pembe degrade
        borderColor: "rgba(236, 72, 153, 1)",
        pointBackgroundColor: "#fff",
        pointBorderColor: "rgba(236, 72, 153, 1)",
        pointRadius: 5,
        pointHoverRadius: 7,
        tension: 0.35,
        borderWidth: 3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "rgba(30, 41, 59, 0.9)", // koyu lacivert tooltip
        titleColor: "#fff",
        bodyColor: "#fff",
        borderColor: "rgba(236, 72, 153, 1)",
        borderWidth: 1,
        padding: 12,
        displayColors: false,
      },
    },
    scales: {
      x: {
        ticks: { color: "#6B7280", font: { size: 12 } },
        grid: { display: false }, // ❌ arka çizgiler kaldırıldı
      },
      y: {
        ticks: { color: "#6B7280", font: { size: 12 } },
        grid: {
          color: "rgba(236, 72, 153, 0.05)", // çok soft pembe çizgi
          borderDash: [4, 4], // dotted stil
        },
      },
    },
  };

  return (
    <div className="max-w-5xl mx-auto p-8 bg-white rounded-2xl shadow-xl border border-pink-100">
      {/* Başlık */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-pink-50">
            <ShoppingCart className="text-pink-500" size={22} />
          </div>
          <h2 className="text-xl font-bold text-gray-800">Günlük Sepete Eklemeler</h2>
        </div>

        {/* Tarih ve buton */}
        <div className="flex items-center gap-3">
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-pink-300"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-pink-300"
          />
          <button
            onClick={fetchData}
            className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg shadow transition"
          >
            Getir
          </button>
        </div>
      </div>

      {/* Grafik */}
      <Line data={chartData} options={chartOptions} height={120} />
    </div>
  );
}
