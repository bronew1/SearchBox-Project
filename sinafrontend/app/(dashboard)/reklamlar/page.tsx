"use client";
import { useEffect, useState } from "react";

export default function AdsTable() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);

  // Backend API base URL (senin domainin)
  const API_BASE = "https://searchprojectdemo.com/api/ads";

  // Google Ads verilerini çek
  async function fetchAds() {
    try {
      const res = await fetch(`${API_BASE}/ads-data/`, {
        credentials: "include",
      });

      if (res.status === 401) {
        // Kullanıcı Google hesabını bağlamamış
        setConnected(false);
        setData([]);
        return;
      }

      // JSON mu kontrol et
      const contentType = res.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const json = await res.json();
        setData(json.data || []);
        setConnected(true);
      } else {
        // JSON yerine HTML dönüyorsa hata/log kaydı
        console.error("JSON yerine HTML döndü:", await res.text());
        setConnected(false);
        setData([]);
      }
    } catch (err) {
      console.error("Veri alınırken hata:", err);
      setConnected(false);
      setData([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchAds();
  }, []);

  if (loading) return <p className="p-4">Yükleniyor...</p>;

  if (!connected) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h2 className="text-lg font-semibold mb-4">
          Reklam verilerini görmek için önce Google hesabınızı bağlayın
        </h2>
        <a
          href={`${API_BASE}/google-login/`}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Google ile Bağlan
        </a>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Google Ads Kampanyaları</h1>

      {data.length === 0 ? (
        <p>Henüz veri yok.</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr>
              <th className="border p-2">Campaign ID</th>
              <th className="border p-2">Name</th>
              <th className="border p-2">Clicks</th>
              <th className="border p-2">Impressions</th>
              <th className="border p-2">CTR</th>
              <th className="border p-2">Avg CPC</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row: any, i: number) => (
              <tr key={i}>
                <td className="border p-2">{row.campaign_id}</td>
                <td className="border p-2">{row.campaign_name}</td>
                <td className="border p-2">{row.clicks}</td>
                <td className="border p-2">{row.impressions}</td>
                <td className="border p-2">
                  {row.impressions > 0
                    ? ((row.clicks / row.impressions) * 100).toFixed(2) + "%"
                    : "0%"}
                </td>
                <td className="border p-2">
                  {row.clicks > 0 ? (row.cost / row.clicks).toFixed(2) : "0"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
