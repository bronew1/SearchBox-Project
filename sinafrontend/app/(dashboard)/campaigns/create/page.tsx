"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Template = {
  id: number;
  title: string;
};

export default function CreateCampaignPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [form, setForm] = useState({
    title: "",
    subject: "",
    html_content: "",
    segment: "cart",
    send_after_days: 1,
    price_limit: "",
    price_condition: "",
    selected_template: "",
    template_mode: "",
    subscriber_time_filter: "", // 🆕 Yeni alan
  });

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/campains/?is_template=true")
      .then((res) => res.json())
      .then((data) => setTemplates(data))
      .catch((err) => console.error("Şablon çekme hatası:", err));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    let html_content = form.html_content;

    if (form.template_mode === "existing" && form.selected_template) {
      const res = await fetch(`https://searchprojectdemo.com/api/campains/${form.selected_template}/`);
      const data = await res.json();
      html_content = data.html_content;
    }

    const payload = {
      ...form,
      html_content,
      is_template: false,
    };

    await fetch("https://searchprojectdemo.com/api/campains/create/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    alert("Kampanya oluşturuldu!");
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Yeni Mail Push Kampanyası</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="title" placeholder="Kampanya Başlığı" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full" required />
        <input name="subject" placeholder="Mail Konusu" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full" required />

        <select name="template_mode" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full">
          <option value="">Kullanım Şekli Seç</option>
          <option value="existing">Var Olan Şablon Seç</option>
          <option value="new">Yeni Şablon Oluştur</option>
          <option value="html">HTML İçerik Yaz</option>
        </select>

        {form.template_mode === "existing" && (
          <select name="selected_template" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full">
            <option value="">Şablon Seç</option>
            {templates.map((t) => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
        )}

        {form.template_mode === "new" && (
          <Link href="/campaigns/new">
            <button type="button" className="bg-green-500 text-white px-4 py-2 rounded">Yeni Şablon Oluştur</button>
          </Link>
        )}

        {form.template_mode === "html" && (
          <textarea name="html_content" placeholder="HTML İçerik" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full h-40" />
        )}

        <select name="segment" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full">
          <option value="cart">Sepete Ekleyenler</option>
          <option value="viewers">Ürünü Görüntüleyenler</option>
          <option value="members">Sadece Üyeler</option>
        </select>

        <input name="send_after_days" type="number" placeholder="Kaç gün sonra gönderilsin?" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full" />

        <input name="price_limit" type="number" placeholder="Fiyat limiti (örn: 5000)" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full" />

        <select name="price_condition" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full">
          <option value="">Fiyat Koşulu Seç</option>
          <option value="higher">Daha yüksek</option>
          <option value="lower">Daha düşük</option>
        </select>

        {/* 🆕 Yeni zaman filtresi alanı */}
        <select name="subscriber_time_filter" onChange={handleChange} className="border border-pink-300 p-2 rounded w-full">
          <option value="">Kime Gönderilsin?</option>
          <option value="all">Tüm Aboneler</option>
          <option value="1d">Son 1 Gün</option>
          <option value="3d">Son 3 Gün</option>
          <option value="7d">Son 7 Gün</option>
          <option value="30d">Son 30 Gün</option>
        </select>

        <button type="submit" className="bg-pink-500 text-white px-4 py-2 rounded">Kaydet</button>
      </form>
    </div>
  );
}
