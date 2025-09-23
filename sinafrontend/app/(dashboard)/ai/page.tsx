"use client";

import { useState } from "react";

export default function AskPage() {
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);

    // kullanıcı mesajını ekle
    setMessages((prev) => [...prev, { role: "user", content: question }]);

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
      const answer = data.answer || "Yanıt alınamadı.";

      // asistan mesajını ekle
      setMessages((prev) => [...prev, { role: "assistant", content: answer }]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Sunucu hatası: " + err.message },
      ]);
    } finally {
      setQuestion("");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] w-full bg-gray-50">
      {/* Mesajlar */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-xl shadow text-sm whitespace-pre-line ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white text-gray-800 border rounded-bl-none"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="px-4 py-2 bg-white border rounded-2xl text-gray-400 text-sm">
              Yazıyor...
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t bg-white p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Bir şey sor..."
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition"
          >
            {loading ? "..." : "Gönder"}
          </button>
        </div>
      </div>
    </div>
  );
}
