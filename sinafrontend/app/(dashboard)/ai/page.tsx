"use client";
import { useState } from "react";

export default function AIPage() {
  const [q, setQ] = useState("");              // Kullanıcının sorusu
  const [a, setA] = useState<string | null>(null); // Model cevabı
  const [loading, setLoading] = useState(false);

  async function ask() {
    if (!q.trim()) return;
    setLoading(true);
    setA(null);

    try {
      const res = await fetch(
        process.env.NEXT_PUBLIC_BACKEND + "/api/ai/ask/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q }),
        }
      );

      if (!res.ok) {
        throw new Error("Backend hatası");
      }

      const data = await res.json();
      setA(data.answer);
    } catch (err) {
      setA("⚠️ Bir hata oluştu: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">CXP AI Asistan</h1>

      {/* Soru input alanı */}
      <div className="flex gap-2">
        <input
          type="text"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Örn: Son 7 günde ROAS değerim ne?"
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          onClick={ask}
          disabled={loading}
          className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
        >
          {loading ? "Soruluyor..." : "Sor"}
        </button>
      </div>

      {/* Cevap alanı */}
      {a && (
        <div className="border rounded p-4 bg-gray-50 whitespace-pre-wrap">
          {a}
        </div>
      )}
    </div>
  );
}
