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
        <h2>devam ediyor...</h2>
    </div>
  );
}
