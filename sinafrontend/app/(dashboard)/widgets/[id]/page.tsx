"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";

export default function EditWidgetProduct() {
  const router = useRouter();
  const params = useParams();
  const { id } = params;

  const [form, setForm] = useState<any>(null);

  useEffect(() => {
    fetch(`https://searchprojectdemo.com/api/widget-products/`)
      .then(res => res.json())
      .then(data => {
        const product = data.find((p: any) => String(p.id) === String(id));
        setForm(product);
      })
      .catch(err => console.error(err));
  }, [id]);

  if (!form) return <div className="p-6">Yükleniyor...</div>;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch("https://searchprojectdemo.com/api/widget-products/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    router.push("/widgets");
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Widget Ürünü Düzenle</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" value={form.name} placeholder="Ürün Adı" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="image_url" value={form.image_url} placeholder="Görsel URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="hover_image_url" value={form.hover_image_url || ""} placeholder="Hover Görsel URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="price" value={form.price} placeholder="Fiyat" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" required />
        <input name="product_url" value={form.product_url || ""} placeholder="Ürün URL" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="sku" value={form.sku || ""} placeholder="SKU" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />
        <input name="order" type="number" value={form.order} placeholder="Sıra" onChange={handleChange} className="border-2 border-pink-500 p-2 w-full rounded" />

        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Güncelle</button>
      </form>
    </div>
  );
}
