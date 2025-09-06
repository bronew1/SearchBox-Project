"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type WidgetProduct = {
  id: number;
  name: string;
  image_url: string;
  price: string;
  sku: string;
  order: number;
};

export default function WidgetProductsPage() {
  const [products, setProducts] = useState<WidgetProduct[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/widget-products/")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-6">
      {/* Başlık */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-xl font-semibold text-gray-800">Widget Ürünleri</h1>
        <Link href="/widgets/create">
          <button className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm transition">
            Yeni Ürün Ekle
          </button>
        </Link>
      </div>

      {/* Kartlar */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition"
          >
            {/* Görsel */}
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-44 object-contain mb-3 rounded-lg"
            />

            {/* Ürün Bilgileri */}
            <h2 className="font-medium text-gray-900 text-base line-clamp-2">
              {product.name}
            </h2>
            <p className="text-gray-700 font-semibold mt-1">{product.price} ₺</p>
            <p className="text-gray-500 text-sm">SKU: {product.sku}</p>
            <p className="text-gray-400 text-xs">Sıra: {product.order}</p>

            {/* Butonlar */}
            <div className="flex gap-2 mt-4">
              <Link href={`/widgets/${product.id}`}>
                <button className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm transition">
                  Düzenle
                </button>
              </Link>
              <button
                className="flex-1 bg-gray-100 hover:bg-red-100 text-red-600 px-3 py-2 rounded-md text-sm transition"
                onClick={async () => {
                  if (confirm("Bu ürünü silmek istediğine emin misin?")) {
                    await fetch(
                      `https://searchprojectdemo.com/api/widget-products/${product.id}/`,
                      { method: "DELETE" }
                    );
                    setProducts(products.filter((p) => p.id !== product.id));
                  }
                }}
              >
                Sil
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
