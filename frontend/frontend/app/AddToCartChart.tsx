"use client"
import { useEffect, useState } from "react"
import { Line } from "react-chartjs-2"
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend)

export default function AddToCartChart() {
  const [chartData, setChartData] = useState<any>(null)

  useEffect(() => {
    fetch("/api/daily-add-to-cart-stats/") // Django endpoint
      .then(res => res.json())
      .then(data => {
        const labels = data.map((d: any) => d.day)
        const counts = data.map((d: any) => d.count)

        setChartData({
          labels,
          datasets: [
            {
              label: "Sepete Ekleme",
              data: counts,
              borderColor: "#6366f1",
              backgroundColor: "#a5b4fc",
              fill: true,
              tension: 0.4,
            }
          ]
        })
      })
  }, [])

  if (!chartData) return <p>Yükleniyor...</p>

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-semibold mb-2">📦 Günlük Sepete Ekleme</h2>
      <Line data={chartData} />
    </div>
  )
}
