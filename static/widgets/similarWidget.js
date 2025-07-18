(function () {
  console.log("🛠️ Benzer ürün widget başlatıldı...");

  // GTM üzerinden gelen view_item event'inden product_id (SKU) çek
  const dataLayerEvents = window.dataLayer?.slice().reverse();
  const viewItemEvent = dataLayerEvents?.find(ev => ev.event === "view_item" && ev.product_id);

  if (!viewItemEvent) {
    console.error("❌ SKU bulunamadı, widget durduruldu.");
    return;
  }

  const sku = viewItemEvent.product_id;
  console.log("✅ SKU bulundu:", sku);

  // API'den benzer ürünleri al
  fetch(`https://searchprojectdemo.com/api/recommendations/similar/${sku}`)
    .then(response => response.json())
    .then(data => {
      if (!data.products || data.products.length === 0) {
        console.log("ℹ️ Benzer ürün bulunamadı.");
        return;
      }

      // .vertical-tab alanını bul
      const container = document.querySelector(".vertical-tab");
      if (!container) {
        console.error("❌ .vertical-tab elementi bulunamadı.");
        return;
      }

      // Widget HTML'ini oluştur
      const widget = document.createElement("div");
      widget.className = "similar-products-widget";
      widget.style.marginTop = "40px";
      widget.innerHTML = `
        <h4 style="margin-bottom: 12px; font-weight: bold;">Benzer Ürünler</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 16px;">
          ${data.products.map(p => `
            <a href="${p.url}" target="_blank" style="text-decoration: none; color: inherit;">
              <div style="width: 160px; border: 1px solid #eee; border-radius: 8px; padding: 10px; text-align: center;">
                <img src="${p.image}" alt="${p.name}" style="width: 100%; height: auto; border-radius: 4px;" />
                <p style="font-size: 14px; margin: 6px 0;">${p.name}</p>
                <strong style="color: #c00;">${Math.round(p.price).toLocaleString('tr-TR')} TL</strong>
              </div>
            </a>
          `).join('')}
        </div>
      `;

      // Widget'ı container'a ekle
      container.appendChild(widget);
      console.log("✅ Benzer ürün widget gösterildi.");
    })
    .catch(err => {
      console.error("❌ Benzer ürünler API çağrısında hata:", err);
    });
})();
