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

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default function DashboardPage() {
  const [data, setData] = useState<any[]>([]);
  const [startDate, setStartDate] = useState("2025-06-01");
  const [endDate, setEndDate] = useState("2025-07-01");

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
        backgroundColor: "rgba(236, 72, 153, 0.2)", // Tailwind pink-500 alpha
        borderColor: "rgba(236, 72, 153, 1)",
        pointBackgroundColor: "white",
        pointBorderColor: "rgba(236, 72, 153, 1)",
        pointRadius: 5,
        tension: 0.4,
        borderWidth: 3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: "#374151", // Tailwind gray-700
          font: {
            size: 14,
          },
        },
      },
      tooltip: {
        backgroundColor: "rgba(17, 24, 39, 0.8)", // Tailwind gray-900
        titleColor: "#fff",
        bodyColor: "#fff",
        borderColor: "rgba(236, 72, 153, 1)",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#6B7280",
        },
        grid: {
          color: "rgba(203, 213, 225, 0.3)",
        },
      },
      y: {
        ticks: {
          color: "#6B7280",
        },
        grid: {
          color: "rgba(203, 213, 225, 0.3)",
        },
      },
    },
  };

  return (
    <div className="max-w-4xl mx-auto py-10 bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-bold mb-6">Günlük Sepete Eklemeler</h2>
      <div className="mb-6 flex flex-wrap gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Başlangıç Tarihi</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border p-2 rounded w-44"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Bitiş Tarihi</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border p-2 rounded w-44"
          />
        </div>
        <button
          onClick={fetchData}
          className="bg-pink-500 text-white px-5 py-2 rounded self-end mt-1"
        >
          Getir
        </button>
      </div>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}
