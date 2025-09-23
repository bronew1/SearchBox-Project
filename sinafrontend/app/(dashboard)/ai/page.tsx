"use client";

import { useState } from "react";

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer(null);
    setProducts([]);

    try {
      const res = await fetch(
        process.env.NEXT_PUBLIC_BACKEND + "/api/aicxp/ask/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
        }
      );

      const data = await res.json();
      if (data.error) {
        setAnswer("⚠️ Hata: " + data.error);
      } else {
        setAnswer(data.answer);
        setProducts(data.products || []);
      }
    } catch (err: any) {
      setAnswer("⚠️ Sunucu hatası: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI Asistan</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 border p-2 rounded"
          placeholder="Bir soru sor... (ör: tektaş ürünleri listele)"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Soruluyor..." : "Sor"}
        </button>
      </div>

      {answer && (
        <div className="mb-6 p-4 bg-gray-100 rounded shadow">
          <h2 className="font-semibold">Yanıt:</h2>
          <p>{answer}</p>
        </div>
      )}

      {products.length > 0 && (
        <div>
          <h2 className="font-semibold mb-2">İlgili Ürünler:</h2>
          <ul className="grid grid-cols-2 gap-4">
            {products.map((p) => (
              <li
                key={p.id}
                className="border rounded p-3 bg-white shadow hover:shadow-lg transition"
              >
                <p className="font-bold">{p.title}</p>
                <p className="text-sm text-gray-600">{p.content}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
