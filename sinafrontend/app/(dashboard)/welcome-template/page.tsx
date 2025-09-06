"use client";
import { useEffect, useState } from "react";
import { Mail } from "lucide-react";

interface TemplateData {
  name: string;
  subject: string;
  html_content: string;
}

export default function WelcomeMailPage() {
  const [template, setTemplate] = useState<TemplateData | null>(null);
  const [loading, setLoading] = useState(true);

  const [name, setName] = useState("");
  const [subject, setSubject] = useState("");
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/subscribe/welcome-template/")
      .then((res) => res.json())
      .then((data) => {
        setTemplate(data);
        setName(data.name);
        setSubject(data.subject);
        setHtmlContent(data.html_content);
        setLoading(false);
      })
      .catch((err) => {
        console.error("API error:", err);
        setLoading(false);
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const updatedData = { name, subject, html_content: htmlContent };

    try {
      const res = await fetch(
        "https://searchprojectdemo.com/api/subscribe/welcome-template/update/",
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updatedData),
        }
      );

      if (res.ok) {
        alert("Şablon başarıyla güncellendi ✅");
      } else {
        alert("Güncelleme sırasında bir hata oluştu.");
      }
    } catch (err) {
      console.error("Update error:", err);
      alert("Bir hata oluştu.");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64 text-gray-400">
        Yükleniyor...
      </div>
    );
  }

  if (!template) {
    return (
      <div className="p-6 text-red-500 text-center">Veri bulunamadı.</div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-10 bg-gradient-to-b from-white to-gray-50 rounded-2xl shadow-md border border-gray-100">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="bg-pink-100 p-3 rounded-full">
          <Mail className="w-6 h-6 text-pink-600" />
        </div>
        <div>
          <h2 className="text-2xl font-semibold text-gray-800">
            Hoşgeldin Mail Şablonu Düzenle
          </h2>
          <p className="text-sm text-gray-500">
            Yeni kullanıcılar için hoş geldin e-postanı burada özelleştirebilirsin.
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Şablon Adı
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Konu Başlığı
          </label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700">
            HTML İçeriği
          </label>
          <textarea
            value={htmlContent}
            onChange={(e) => setHtmlContent(e.target.value)}
            rows={12}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 bg-gray-50 font-mono text-sm shadow-inner focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition"
          ></textarea>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-pink-600 text-white px-6 py-3 rounded-lg font-semibold shadow hover:bg-pink-700 transition transform hover:scale-[1.01]"
          >
            Güncelle
          </button>
        </div>
      </form>
    </div>
  );
}
