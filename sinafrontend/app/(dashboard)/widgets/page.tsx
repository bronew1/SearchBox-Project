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
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Widget Ürünleri</h1>
        <Link href="/widgets/create">
          <button className="bg-pink-500 text-white px-4 py-2 rounded">Yeni Ürün Ekle</button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map(product => (
          <div
            key={product.id}
            className="border-4 border-pink-500 rounded-2xl p-4 shadow"
          >
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-40 object-cover mb-2 rounded-2xl"
            />
            <h2 className="font-bold text-lg">{product.name}</h2>
            <p className="text-gray-600">Fiyat: {product.price}₺</p>
            <p className="text-gray-600">SKU: {product.sku}</p>
            <p className="text-gray-500 text-sm">Sıra: {product.order}</p>

            <div className="flex gap-2 mt-4">
              <Link href={`/widgets/${product.id}`}>
                <button className="bg-blue-500 text-white px-3 py-1 rounded">
                  Düzenle
                </button>
              </Link>
              <button
                className="bg-red-500 text-white px-3 py-1 rounded"
                onClick={async () => {
                  if (confirm("Bu ürünü silmek istediğine emin misin?")) {
                    await fetch(`https://searchprojectdemo.com/api/widget-products/${product.id}/`, {
                      method: "DELETE",
                    });
                    setProducts(products.filter(p => p.id !== product.id));
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
