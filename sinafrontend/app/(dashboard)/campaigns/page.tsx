"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Campaign = {
  id: number;
  title: string;
  subject: string;
  segment: string;
  send_after_days: number;
  created_at: string;
};

export default function CampaignListPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/campains/")
      .then((res) => res.json())
      .then((data) => setCampaigns(data))
      .catch((err) => console.error("Kampanya çekme hatası:", err));
  }, []);

  const handleDelete = async (id: number) => {
    const confirmed = confirm("Bu kampanyayı silmek istediğinize emin misiniz?");
    if (!confirmed) return;

    try {
      const res = await fetch(`https://searchprojectdemo.com/api/campains/delete/${id}/`, {
        method: "DELETE",
      });

      if (res.ok) {
        setCampaigns(campaigns.filter((c) => c.id !== id));
        alert("Kampanya başarıyla silindi.");
      } else {
        console.error("Silme hatası:", await res.text());
        alert("Kampanya silinirken bir hata oluştu.");
      }
    } catch (error) {
      console.error("Silme error:", error);
      alert("Kampanya silinirken bir hata oluştu.");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Kampanya Listesi</h1>

      <div className="flex gap-4 mb-4">
        <Link href="/campaigns/create">
          <button className="bg-green-500 text-white px-4 py-2 rounded">Yeni Kampanya Ekle</button>
        </Link>

        <Link href="/campaigns/sablonlar">
          <button className="bg-pink-500 text-white px-4 py-2 rounded">Şablonlarım</button>
        </Link>
      </div>

      {campaigns.length === 0 ? (
        <p>Henüz bir kampanya yok.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {campaigns.map((c) => (
            <div
              key={c.id}
              className="border-2 border-pink-300 rounded-lg p-4 shadow hover:shadow-lg transition hover:bg-pink-50"
            >
              <Link href={`/campaigns/${c.id}`} className="block">
                <div className="flex flex-col md:flex-row justify-between items-center">
                  <div className="flex-1">
                    <h2 className="font-bold text-xl mb-1">{c.title}</h2>
                    <p className="text-gray-700"><b>Konu:</b> {c.subject}</p>
                    <p className="text-gray-700"><b>Segment:</b> {c.segment}</p>
                  </div>
                  <div className="flex flex-col items-end mt-2 md:mt-0 md:ml-4 text-right">
                    <p className="text-gray-700"><b>Kaç gün sonra:</b> {c.send_after_days} gün</p>
                    <p className="text-gray-700"><b>Oluşturma:</b> {c.created_at}</p>
                  </div>
                </div>
              </Link>

              <button
                onClick={() => handleDelete(c.id)}
                className="mt-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              >
                Sil
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
