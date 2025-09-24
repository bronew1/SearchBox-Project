"use client";

import { useState } from "react";
import { Send } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function AskPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);

    const newUserMessage: Message = { role: "user", content: question };
    setMessages((prev) => [...prev, newUserMessage]);

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

      const newAssistantMessage: Message = { role: "assistant", content: answer };
      setMessages((prev) => [...prev, newAssistantMessage]);
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
    <div className="flex flex-col h-screen bg-gradient-to-b from-white to-[#ebbecb]/20">
      {/* Logo ve başlık */}
      <div className="flex flex-col items-center mt-10">
        <img
          src="https://www.sinapirlanta.com/themes/custom/sina/logo.svg"
          alt="Sina Pırlanta"
          className="w-20 h-20 mb-4"
        />
        <h1 className="text-lg font-semibold text-gray-800">
          Sina Pırlanta SinAI
        </h1>
      </div>

      {/* Mesajlar */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 max-w-3xl w-full mx-auto">
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
                  ? "bg-[#f7e5ea] text-gray-800 rounded-br-none" // 🎨 kullanıcı balonu
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
        <div className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#ebbecb]"
            placeholder="Bir şey sor..."
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-[#ebbecb] text-white px-6 py-2 rounded-full hover:bg-pink-400 transition disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
