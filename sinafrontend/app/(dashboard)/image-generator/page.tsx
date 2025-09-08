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
    <div className="flex">
      {/* Sol panel */}
      <div className="w-1/3 p-4 border-r">
        <h2 className="font-bold mb-2">Reklam Oluştur</h2>
        <input
          type="text"
          placeholder="Prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="CTA"
          value={cta}
          onChange={(e) => setCta(e.target.value)}
          className="border p-2 mb-2 w-full"
        />
        <input
          type="text"
          placeholder="Slogan"
          value={slogan}
          onChange={(e) => setSlogan(e.target.value)}
          className="border p-2 mb-2 w-full"
        />
        <select
          value={size}
          onChange={(e) => setSize(e.target.value)}
          className="border p-2 mb-2 w-full"
        >
          <option value="1:1">1:1 (Square)</option>
          <option value="16:9">16:9 (Wide)</option>
          <option value="9:16">9:16 (Story)</option>
        </select>
        <button
          onClick={handleGenerate}
          className="bg-green-500 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Oluşturuluyor..." : "Görsel Oluştur"}
        </button>
      </div>

      {/* Sağ panel */}
      <div className="w-2/3 p-4 flex justify-center items-center">
        {loading && <p>⏳ Görsel oluşturuluyor...</p>}
        {imageUrl && <img src={imageUrl} alt="Generated Ad" className="max-w-full" />}
      </div>
    </div>
  );
}
