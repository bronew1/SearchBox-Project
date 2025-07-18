(function () {
  console.log("🛠️ Benzer ürün widget başlatıldı...");

  // GTM'den gelen son view_item event'inden product_id çek
  const dataLayerEvents = window.dataLayer?.slice().reverse();
  const viewItem = dataLayerEvents?.find(ev => ev.event === "view_item" && ev.product_id);

  if (!viewItem) {
    console.error("❌ product_id bulunamadı, widget durduruldu.");
    return;
  }

  const productId = viewItem.product_id;
  console.log("✅ product_id bulundu:", productId);

  // Benzer ürün API çağrısı
  fetch(`https://searchprojectdemo.com/api/also-viewed-products/${productId}`)
    .then(res => res.json())
    .then(data => {
      if (!data || data.length === 0) {
        console.log("ℹ️ Benzer ürün bulunamadı.");
        return;
      }

      const container = document.querySelector(".vertical-tab");
      if (!container) {
        console.error("❌ .vertical-tab elementi bulunamadı.");
        return;
      }

      const widget = document.createElement("div");
      widget.className = "similar-products-widget";
      widget.style.marginTop = "40px";

      widget.innerHTML = `
        <h4 style="font-weight: bold; font-size: 16px; margin-bottom: 12px;">Benzer Ürünler</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 16px;">
          ${data.map(p => `
            <a href="/urun/${p.id}" style="text-decoration: none; color: inherit;" target="_blank">
              <div style="width: 160px; border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center;">
                <img src="${p.image_url}" style="width: 100%; height: auto; border-radius: 6px;" />
                <div style="font-size: 14px; margin-top: 6px;">${p.name}</div>
                <div style="font-weight: bold; color: #c00;">${Math.round(p.price).toLocaleString('tr-TR')} TL</div>
              </div>
            </a>
          `).join("")}
        </div>
      `;

      container.appendChild(widget);
      console.log("✅ Benzer ürün widget başarıyla gösterildi.");
    })
    .catch(err => {
      console.error("❌ API çağrısında hata:", err);
    });
})();
