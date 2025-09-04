"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

declare global {
  interface Window {
    unlayer: any;
  }
}

type Template = {
  id: number;
  title: string;
  html_content: string;
  design_json?: any;
  created_at: string;
};

export default function TemplateDetailPage() {
  const [template, setTemplate] = useState<Template | null>(null);
  const unlayerRef = useRef<any>(null);
  const params = useParams();

  useEffect(() => {
    const templateId = params?.id;
    if (!templateId) return;

    fetch(`https://searchprojectdemo.com/api/campains/${templateId}/`)
      .then((res) => res.json())
      .then((data) => setTemplate(data))
      .catch((err) => console.error("Şablon çekme hatası:", err));
  }, [params]);

  useEffect(() => {
    if (!template || typeof window === "undefined" || !window.unlayer) return;

    // Editor container'ı temizle
    const container = document.getElementById("editor-container");
    if (container) {
      container.innerHTML = '<div id="editor"></div>';
    }

    // Init
    window.unlayer.init({
      id: "editor",
      displayMode: "email",
      height: "100%",
      source: template.design_json ? { design: template.design_json } : undefined,
      // Mobil & tablet önizleme modlarını aktif et
      features: {
        preview: true
      },
      // Eğer önceden kaydedilmiş HTML varsa loadDesign çağırma
      // (sadece design_json varsa yükle, yoksa source: html kullan)
    });

    if (template.design_json) {
      window.unlayer.loadDesign(template.design_json);
    } else if (template.html_content) {
      window.unlayer.loadDesign({ html: template.html_content });
    }

    unlayerRef.current = window.unlayer;
  }, [template]);

  if (!template) return <div className="p-6">Yükleniyor...</div>;

  return (
    <div className="p-6 h-screen flex flex-col">
      <h1 className="text-2xl font-bold mb-4">{template.title}</h1>

      <div
        id="editor-container"
        className="flex-1"
        style={{
          minHeight: "700px",
          border: "1px solid #f3a4c3",
          borderRadius: "8px",
          overflow: "hidden",
        }}
      >
        <div id="editor" style={{ height: "100%", width: "100%" }} />
      </div>

      <p className="text-gray-500 text-sm mt-2">Oluşturma: {template.created_at}</p>

      <Link href="/campaigns/sablonlar">
        <button className="mt-4 bg-pink-500 text-white px-4 py-2 rounded">Geri Dön</button>
      </Link>
    </div>
  );
}
