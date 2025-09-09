"use client";

import { useEffect, useMemo, useRef, useState } from "react";

type JobStatus = "queued" | "processing" | "completed" | "failed";

export default function AdGenerator() {
  // form state
  const [purpose, setPurpose] = useState("");
  const [adType, setAdType] = useState("");
  const [prompt, setPrompt] = useState("");
  const [cta, setCta] = useState("");
  const [slogan, setSlogan] = useState("");
  const [size, setSize] = useState("1:1");

  // ui state
  const [activeTab, setActiveTab] = useState<"design" | "library">("design");
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);

  // setInterval tipi: Node/DOM çakışması yok
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const stopPolling = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  };

  const startJob = async () => {
    setLoading(true);
    setImageUrl("");

    const res = await fetch("http://127.0.0.1:8000/api/ads/generate-ad/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        cta,
        slogan,
        size,
        purpose,
        ad_type: adType,
      }),
    });
    const data = await res.json();
    const id: string = data.id;

    pollRef.current = setInterval(async () => {
      const r = await fetch(`http://127.0.0.1:8000/api/ads/jobs/${id}/`);
      const job = await r.json();
      const status: JobStatus = job.status;

      if (status === "completed") {
        stopPolling();
        setImageUrl(job.result_url);
        setLoading(false);
      } else if (status === "failed") {
        stopPolling();
        setLoading(false);
        alert("❌ Görsel oluşturulamadı: " + (job.error ?? "Bilinmeyen hata"));
      }
    }, 3000);
  };

  const handleGenerate = () => startJob();
  const handleRegenerate = () => startJob();

  const handleDownload = () => {
    if (!imageUrl) return;
    const a = document.createElement("a");
    a.href = imageUrl;
    a.download = "reklam-gorseli.png";
    a.target = "_blank";
    a.rel = "noopener";
    a.click();
  };

  useEffect(() => () => stopPolling(), []);

  // checkerboard rengi: #ebbecb (soft)
  const checkerStyle = useMemo(
    () => ({
      backgroundImage: `
        linear-gradient(90deg, rgba(235,190,203,.35) 25%, transparent 25%, transparent 75%, rgba(235,190,203,.35) 75%),
        linear-gradient(0deg,  rgba(235,190,203,.35) 25%, transparent 25%, transparent 75%, rgba(235,190,203,.35) 75%)
      `,
      backgroundSize: "120px 120px",
      backgroundPosition: "0 0, 60px 60px",
    }),
    []
  );

  return (
    <div className="flex h-full min-h-0 bg-[#f7f8f9]">
      {/* Sol panel */}
      <aside className="w-[360px] min-w-[300px] border-r bg-white overflow-auto">
        <div className="p-5 md:p-6">
          <h2 className="text-[15px] font-semibold mb-3">Reklamın Amacı</h2>
          <select
            value={purpose}
            onChange={(e) => setPurpose(e.target.value)}
            className="w-full h-11 rounded-lg border px-3 text-sm"
          >
            <option value="">Bir seçenek seçin</option>
            <option>Satış Odaklı</option>
            <option>Marka Bilinirliği</option>
            <option>Tıklama / Trafik</option>
          </select>

          <h2 className="text-[15px] font-semibold mt-6 mb-3">Reklam Türü</h2>
          <select
            value={adType}
            onChange={(e) => setAdType(e.target.value)}
            className="w-full h-11 rounded-lg border px-3 text-sm"
          >
            <option value="">Bir seçenek seçin</option>
            <option>Tek Görsel</option>
            <option>Kare (Katalog)</option>
            <option>Hikâye / Reels</option>
          </select>

          <h2 className="text-[15px] font-semibold mt-6 mb-2">
            Reklamı Açıkla - Prompt
          </h2>
          <div className="relative">
            <textarea
              placeholder="Yeşil bir park, spor ayakkabı, 'Şimdi Satın Al' butonu, beyaz arkaplan..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={3}
              className="w-full rounded-lg border px-3 py-3 pr-10 text-sm"
            />
            <button
              type="button"
              className="absolute right-2 top-2.5 inline-flex h-8 w-8 items-center justify-center rounded-md border bg-white text-gray-500"
              title="Prompt sihirbazı"
            >
              ✨
            </button>
          </div>

          <h2 className="text-[15px] font-semibold mt-6 mb-2">CTA</h2>
          <input
            type="text"
            placeholder="Satın Almak için Tıkla"
            value={cta}
            onChange={(e) => setCta(e.target.value)}
            className="w-full h-11 rounded-lg border px-3 text-sm"
          />

          <h2 className="text-[15px] font-semibold mt-6 mb-2">Slogan</h2>
          <input
            type="text"
            placeholder="Slogan"
            value={slogan}
            onChange={(e) => setSlogan(e.target.value)}
            className="w-full h-11 rounded-lg border px-3 text-sm"
          />

          <div className="mt-6">
            <button
  onClick={handleGenerate}
  disabled={loading}
  className="w-full h-11 rounded-lg text-white text-sm font-medium disabled:opacity-60"
  style={{
    backgroundColor: "#ebbecb",
    color: "#fff",
  }}
  onMouseEnter={(e) => {
    (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#d9a8b7"; // hover tonu
  }}
  onMouseLeave={(e) => {
    (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#ebbecb";
  }}
>
  {loading ? "⏳ Oluşturuluyor..." : "Görsel Oluştur"}
</button>
            
          </div>
        </div>
      </aside>

      {/* Sağ panel */}
      <main className="flex-1 min-w-0 min-h-0 flex flex-col">
        {/* Üst sekmeler + indir */}
        <div className="flex items-center justify-between px-4 md:px-6 py-3 bg-white border-b">
          <div className="flex items-center gap-2 rounded-lg bg-gray-100 p-1">
            <button
              className={`h-9 px-3 md:px-4 rounded-md text-sm ${
                activeTab === "design" ? "bg-white shadow-sm font-medium" : ""
              }`}
              onClick={() => setActiveTab("design")}
            >
              🔗 Tasarım
            </button>
            <button
              className={`h-9 px-3 md:px-4 rounded-md text-sm ${
                activeTab === "library" ? "bg-white shadow-sm font-medium" : ""
              }`}
              onClick={() => setActiveTab("library")}
            >
              📁 Kütüphane
            </button>
          </div>

          <button
            onClick={handleDownload}
            disabled={!imageUrl}
            className="h-9 w-9 rounded-md border flex items-center justify-center text-gray-600 disabled:opacity-50"
            title="İndir"
          >
            ⬇️
          </button>
        </div>

        {/* Kanvas alanı — taşma yok */}
        <div className="flex-1 min-h-0 overflow-auto">
          <div
            className="m-4 md:m-6 rounded-xl border bg-white shadow-inner flex items-center justify-center"
            style={checkerStyle as React.CSSProperties}
          >
            <div className="w-full max-w-[1200px] mx-auto my-6 md:my-10">
              <div className="mx-auto w-full rounded-xl bg-white/50 p-2">
                <div
                  className="flex items-center justify-center rounded-xl border bg-white/60"
                  style={{ height: "min(70vh, 900px)" }}
                >
                  {loading && (
                    <p className="text-gray-500 font-medium">
                      ⏳ Görsel oluşturuluyor...
                    </p>
                  )}
                  {!loading && imageUrl && (
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
          </div>
        </div>

        {/* Alt bilgi */}
        <div className="flex items-center justify-between px-4 md:px-6 py-3 border-t bg-white">
          <div className="text-sm text-gray-600">
            <div className="font-medium">Adsız Tasarım</div>
            <div className="text-xs text-gray-500">{size}</div>
          </div>

          <div className="flex items-center gap-3">
            <select
              value={size}
              onChange={(e) => setSize(e.target.value)}
              className="h-9 rounded-md border px-3 text-sm"
              title="Boyut"
            >
              <option value="1:1">1:1</option>
              <option value="16:9">16:9</option>
              <option value="9:16">9:16</option>
            </select>

            <button
              onClick={handleRegenerate}
              disabled={loading || !prompt}
              className="inline-flex items-center gap-2 h-9 px-4 rounded-md border text-sm hover:bg-gray-50 disabled:opacity-60"
            >
              ✨ Yeniden Oluştur
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
