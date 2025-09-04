"use client";
import { useEffect, useState } from "react";

interface TemplateData {
  name: string;
  subject: string;
  html_content: string;
}

export default function WelcomeMailPage() {
  const [template, setTemplate] = useState<TemplateData | null>(null);
  const [loading, setLoading] = useState(true);

  // Form state
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
    const updatedData = {
      name,
      subject,
      html_content: htmlContent,
    };

    try {
      const res = await fetch("https://searchprojectdemo.com/api/subscribe/welcome-template/update/", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      });

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
    return <div className="flex justify-center items-center h-64 text-gray-500">Yükleniyor...</div>;
  }

  if (!template) {
    return <div className="p-6 text-red-500 text-center">Veri bulunamadı.</div>;
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-pink-600">Hoşgeldin Mail Şablonu Düzenle</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-1">Şablon Adı</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border rounded-lg p-2 focus:ring focus:ring-pink-200"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Konu Başlığı</label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full border rounded-lg p-2 focus:ring focus:ring-pink-200"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">HTML İçeriği</label>
          <textarea
            value={htmlContent}
            onChange={(e) => setHtmlContent(e.target.value)}
            rows={10}
            className="w-full border rounded-lg p-2 focus:ring focus:ring-pink-200"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full bg-pink-600 text-white py-3 rounded-lg font-semibold hover:bg-pink-700 transition"
        >
          Güncelle
        </button>
      </form>
    </div>
  );
}
