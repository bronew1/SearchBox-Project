"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

type Campaign = {
  id: number;
  title: string;
  subject: string;
  segment: string;
  html_content: string;
  send_after_days: number;
  created_at: string;
  price_limit?: number | null;
  price_condition?: string | null;
};

export default function CampaignDetailPage() {
  const params = useParams();
  const { id } = params;
  const router = useRouter();

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`https://searchprojectdemo.com/api/campains/${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setCampaign(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Detay çekme hatası:", err);
        setLoading(false);
      });
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    if (!campaign) return;
    setCampaign({ ...campaign, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!campaign) return;

    await fetch(`https://searchprojectdemo.com/api/campains/${id}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(campaign),
    });

    alert("Kampanya güncellendi!");
    router.push("/campaigns");
  };

  if (loading) return <div className="p-6">Yükleniyor...</div>;
  if (!campaign) return <div className="p-6">Kampanya bulunamadı.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Kampanya Güncelle</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="title"
          value={campaign.title}
          onChange={handleChange}
          placeholder="Başlık"
          className="border border-pink-300 rounded w-full p-2"
          required
        />

        <input
          type="text"
          name="subject"
          value={campaign.subject}
          onChange={handleChange}
          placeholder="Konu"
          className="border border-pink-300 rounded w-full p-2"
          required
        />

        <select
          name="segment"
          value={campaign.segment}
          onChange={handleChange}
          className="border border-pink-300 rounded w-full p-2"
          required
        >
          <option value="">Segment Seç</option>
          <option value="cart">Sepete Ekleyenler</option>
          <option value="viewers">Ürünü Görüntüleyenler</option>
          <option value="members">Üyeler</option>
        </select>

        <textarea
          name="html_content"
          value={campaign.html_content}
          onChange={handleChange}
          placeholder="HTML İçerik"
          className="border border-pink-300 rounded w-full p-2"
          rows={6}
        />

        <input
          type="number"
          name="send_after_days"
          value={campaign.send_after_days}
          onChange={handleChange}
          placeholder="Kaç gün sonra gönderilsin?"
          className="border border-pink-300 rounded w-full p-2"
          required
        />

        <input
          type="number"
          name="price_limit"
          value={campaign.price_limit ?? ""}
          onChange={handleChange}
          placeholder="Fiyat limiti (örn: 5000)"
          className="border border-pink-300 rounded w-full p-2"
        />

        <select
          name="price_condition"
          value={campaign.price_condition ?? ""}
          onChange={handleChange}
          className="border border-pink-300 rounded w-full p-2"
        >
          <option value="">Fiyat Koşulu Seç</option>
          <option value="higher">Daha yüksek</option>
          <option value="lower">Daha düşük</option>
        </select>

        <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
          Güncelle
        </button>
      </form>

      {/* 💥 Önizleme alanı */}
      {campaign.html_content && (
        <div className="border border-gray-300 rounded p-4 mt-8">
          <h2 className="text-lg font-semibold mb-2">Mail Önizleme</h2>
          <div
            dangerouslySetInnerHTML={{ __html: campaign.html_content }}
          />
        </div>
      )}
    </div>
  );
}
