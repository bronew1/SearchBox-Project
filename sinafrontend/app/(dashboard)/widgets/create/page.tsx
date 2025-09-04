"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CreateWidgetProduct() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    image_url: "",
    hover_image_url: "",
    price: "",
    product_url: "",
    sku: "",
    order: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch("https://searchprojectdemo.com/api/widget-products/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    router.push("/widgets");
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Yeni Widget Ürün Ekle</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" placeholder="Ürün Adı" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="image_url" placeholder="Görsel URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="hover_image_url" placeholder="Hover Görsel URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="price" placeholder="Fiyat" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="product_url" placeholder="Ürün URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="sku" placeholder="SKU" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="order" type="number" placeholder="Sıra" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />

        <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">Kaydet</button>
      </form>
    </div>
  );
}
