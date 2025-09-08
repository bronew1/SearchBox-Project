"use client";

import { useState } from "react";

export default function AdGenerator() {
  const [prompt, setPrompt] = useState("");
  const [cta, setCta] = useState("");
  const [slogan, setSlogan] = useState("");
  const [size, setSize] = useState("1:1");
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setImageUrl("");

    // 1. Yeni job başlat
    const res = await fetch("http://127.0.0.1:8000/api/ads/generate-ad/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, cta, slogan, size }),
    });

    const data = await res.json();
    const jobId = data.id;

    // 2. Job durumunu poll et
    const checkStatus = setInterval(async () => {
      const jobRes = await fetch(`http://127.0.0.1:8000/api/ads/jobs/${jobId}/`);
      const job = await jobRes.json();

      if (job.status === "completed") {
        clearInterval(checkStatus);
        setImageUrl(job.result_url);
        setLoading(false);
      }
      if (job.status === "failed") {
        clearInterval(checkStatus);
        alert("❌ Görsel oluşturulamadı: " + job.error);
        setLoading(false);
      }
    }, 3000);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sol panel */}
      <div className="w-1/3 p-6 border-r bg-white shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Reklam Oluştur</h2>

        <label className="text-sm font-medium">Reklam Açıklaması - Prompt</label>
        <textarea
          placeholder="Yeşil bir park, spor ayakkabı, 'Şimdi Satın Al' butonu..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="border rounded-lg p-3 mb-4 w-full text-sm"
          rows={3}
        />

        <label className="text-sm font-medium">CTA</label>
        <input
          type="text"
          placeholder="Satın Al"
          value={cta}
          onChange={(e) => setCta(e.target.value)}
          className="border rounded-lg p-3 mb-4 w-full text-sm"
        />

        <label className="text-sm font-medium">Slogan</label>
        <input
          type="text"
          placeholder="Slogan girin..."
          value={slogan}
          onChange={(e) => setSlogan(e.target.value)}
          className="border rounded-lg p-3 mb-4 w-full text-sm"
        />

        <label className="text-sm font-medium">Boyut</label>
        <select
          value={size}
          onChange={(e) => setSize(e.target.value)}
          className="border rounded-lg p-3 mb-6 w-full text-sm"
        >
          <option value="1:1">1:1 (Square)</option>
          <option value="16:9">16:9 (Wide)</option>
          <option value="9:16">9:16 (Story)</option>
        </select>

        <button
          onClick={handleGenerate}
          className="bg-green-500 hover:bg-green-600 transition text-white font-medium px-4 py-2 rounded-lg w-full"
          disabled={loading}
        >
          {loading ? "⏳ Oluşturuluyor..." : "🎨 Görsel Oluştur"}
        </button>
      </div>

      {/* Sağ panel */}
      <div className="w-2/3 flex items-center justify-center bg-gray-100">
        <div className="w-[90%] h-[90%] flex items-center justify-center border-2 border-dashed border-gray-300 rounded-xl bg-white shadow-inner">
          {loading && (
            <p className="text-gray-500 font-medium">⏳ Görsel oluşturuluyor...</p>
          )}
          {imageUrl && (
            <img
              src={imageUrl}
              alt="Generated Ad"
              className="max-h-full max-w-full rounded-lg shadow-lg"
            />
          )}
          {!loading && !imageUrl && (
            <p className="text-gray-400">Henüz bir görsel oluşturulmadı</p>
          )}
        </div>
      </div>
    </div>
  );
}
