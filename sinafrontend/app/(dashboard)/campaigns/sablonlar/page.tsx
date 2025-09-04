"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Template = {
  id: number;
  title: string;
  html_content: string;
  design_json: any;
  created_at: string;
};

export default function TemplateListPage() {
  const [templates, setTemplates] = useState<Template[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/campains/?is_template=true")
      .then((res) => res.json())
      .then((data) => setTemplates(data))
      .catch((err) => console.error("Şablon çekme hatası:", err));
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Şablonlarım</h1>
        <Link href="/campaigns/new">
          <button className="bg-pink-500 text-white px-4 py-2 rounded">
            Yeni Şablon Oluştur
          </button>
        </Link>
      </div>

      {templates.length === 0 ? (
        <p>Henüz bir şablon yok.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((t) => (
            <Link href={`/campaigns/sablonlar/${t.id}`} key={t.id}>
              <div className="border-2 border-pink-300 rounded-lg p-4 shadow hover:shadow-lg transition hover:bg-pink-50 cursor-pointer">
                <h2 className="font-bold text-xl mb-2">{t.title}</h2>
                <div className="border p-2 h-64 overflow-hidden bg-white">
                  <iframe
                    sandbox=""
                    srcDoc={t.html_content}
                    style={{ width: "100%", height: "100%", border: "none" }}
                  />
                </div>
                <p className="text-gray-500 text-sm mt-2">
                  Oluşturma: {t.created_at}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
