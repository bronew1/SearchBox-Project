"use client";
import { useEffect, useState } from "react";

export default function BestSellersWidget() {
  const [visible, setVisible] = useState(false);
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    fetch("https://searchprojectdemo.com/api/product/widget-products/")
      .then((res) => res.json())
      .then((data) => setProducts(data.products));
  }, []);

  return (
    <>
      <div
        className="fixed bottom-4 left-4 w-[85px] h-[85px] rounded-full bg-[#ebbecb] shadow-lg flex items-center justify-center cursor-pointer z-50"
        onClick={() => setVisible(!visible)}
      >
        Fırsatlar💎
      </div>

      {visible && (
        <div className="fixed bottom-[100px] left-4 w-[764px] h-[544px] bg-white border rounded-2xl shadow-2xl p-6 overflow-y-auto z-50">
          <h2 className="text-center text-xl font-bold mb-4">ÇOK SATANLAR</h2>
          <div className="grid grid-cols-2 gap-4">
            {products.map((p, i) => (
              <div
                key={i}
                className="border border-[#e6d1d1] p-4 rounded-md product-best-wrapper"
              >
                <div className="relative">
                  <div className="absolute top-2 right-2 space-y-1 text-xs font-bold text-white">
                    <div className="bg-black px-2 py-0.5 rounded">HIZLI KARGO</div>
                    {/* Örnek olarak sabit, istenirse Django modeliyle genişletilebilir */}
                    {/* <div className="bg-[#b94687] px-2 py-0.5 rounded">ÇOK SATAN</div> */}
                    {/* <div className="bg-[#df95b6] px-2 py-0.5 rounded">ÖZEL FİYAT</div> */}
                  </div>

                  <a href={p.url}>
                    <img
                      className="w-full h-auto rounded-md transition-transform duration-300 hover:scale-105"
                      src={p.image_url}
                      alt={p.name}
                    />
                  </a>
                </div>

                <div className="mt-4 text-center">
                  <a
                    href={p.url}
                    className="block text-sm font-medium leading-tight hover:underline"
                  >
                    {p.name}
                  </a>

                  <p className="text-[#b2b2b2] text-sm line-through mt-1">
                    {/* Hardcoded eski fiyat örnek olarak */}
                    {parseFloat(p.price) > 2000 ? "2.990 TL" : "1.990 TL"}
                  </p>

                  <p className="text-black text-xl font-bold">
                    {parseFloat(p.price).toLocaleString("tr-TR")} TL
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
