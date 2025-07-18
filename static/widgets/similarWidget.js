(function () {
  console.log("👀 Benzer ürün widget başlatıldı...");

  window.addEventListener("message", async (event) => {
    if (!event?.data || event.data.event_name !== "view_item") return;

    const { product_id } = event.data;

    if (!product_id) {
      console.error("❌ product_id bulunamadı, widget durduruldu.");
      return;
    }

    console.log("✅ Widget başlatılıyor, product_id:", product_id);

    // Eğer widget zaten varsa tekrar ekleme
    if (document.querySelector("#similar-products-widget")) return;

    // Widget container oluştur
    const widgetContainer = document.createElement("div");
    widgetContainer.id = "similar-products-widget";
    widgetContainer.style.position = "fixed";
    widgetContainer.style.bottom = "20px";
    widgetContainer.style.right = "20px";
    widgetContainer.style.width = "360px";
    widgetContainer.style.maxHeight = "80vh";
    widgetContainer.style.overflowY = "auto";
    widgetContainer.style.backgroundColor = "#fff";
    widgetContainer.style.border = "1px solid #ccc";
    widgetContainer.style.borderRadius = "12px";
    widgetContainer.style.padding = "16px";
    widgetContainer.style.boxShadow = "0 4px 16px rgba(0,0,0,0.2)";
    widgetContainer.style.zIndex = "9999";
    widgetContainer.innerText = "⏳ Yükleniyor...";

    document.body.appendChild(widgetContainer);

    try {
      const res = await fetch(`https://searchprojectdemo.com/api/recommendations/similar/${product_id}/`);
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        widgetContainer.innerText = "Benzer ürün bulunamadı.";
        return;
      }

      widgetContainer.innerHTML = "<h3 style='margin-bottom:12px;'>Benzer Ürünler</h3>";

      data.forEach((item) => {
        const card = document.createElement("div");
        card.style.display = "flex";
        card.style.alignItems = "center";
        card.style.marginBottom = "12px";
        card.style.gap = "12px";
        card.style.borderBottom = "1px solid #eee";
        card.style.paddingBottom = "10px";

        card.innerHTML = `
          <a href="${item.url}" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <img src="${item.image}" alt="${item.name}" width="64" height="64" style="object-fit: cover; border-radius: 8px;" />
            <div style="margin-left: 8px;">
              <p style="margin: 0; font-size: 14px;"><strong>${item.name}</strong></p>
              <p style="margin: 4px 0 0 0; color: #888;">${item.price} TL</p>
            </div>
          </a>
        `;

        widgetContainer.appendChild(card);
      });

    } catch (err) {
      console.error("❌ Widget verisi alınamadı:", err);
      widgetContainer.innerText = "Bir hata oluştu.";
    }
  });
})();
