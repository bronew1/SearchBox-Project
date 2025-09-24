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

    </div>
  );
}
