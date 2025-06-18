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
      {/* Yuvarlak Buton */}
      <div
        className="fixed bottom-4 left-4 w-[85px] h-[85px] rounded-full bg-[#ebbecb] shadow-lg flex items-center justify-center cursor-pointer z-50"
        onClick={() => setVisible(!visible)}
      >
        🛍️
      </div>

      {/* Açılır Panel */}
      {visible && (
        <div className="fixed bottom-[100px] left-4 w-[764px] h-[544px] bg-white border rounded-2xl shadow-2xl p-4 overflow-y-auto z-50">
          <div className="grid grid-cols-2 gap-4">
            {products.map((p, i) => (
              <div key={i} className="product-best-wrapper">
                <div className="product-img">
                  <a href={p.url}>
                    <img
                      className="base-image"
                      src={p.image_url}
                      alt={p.name}
                      width={358}
                      height={358}
                    />
                  </a>
                  <a href={p.url}>
                    <img
                      className="hover-image"
                      src={p.hover_image_url}
                      alt={p.name}
                      width={358}
                      height={358}
                    />
                  </a>
                  <div className="hover-img-detail">
                    <div className="product-code">{p.sku}</div>
                    <div>
                      <a href="#" className="product-fav" data-sku={p.sku}>F</a>
                      <a href={p.url} className="product-sepet">S</a>
                    </div>
                  </div>
                </div>

                <div className="product-detail">
                  <a href={p.url} className="product-title">{p.name}</a>
                  <p className="price-wrapper">
                    <span className="product-price">{p.price} TL</span>
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
