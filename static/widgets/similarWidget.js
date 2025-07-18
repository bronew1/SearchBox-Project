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

    const widgetContainer = document.createElement("div");
    widgetContainer.id = "similar-products-widget";
    widgetContainer.style.border = "1px solid #ccc";
    widgetContainer.style.padding = "10px";
    widgetContainer.innerText = "⏳ Yükleniyor...";

    document.body.appendChild(widgetContainer);

    try {
      const res = await fetch(`https://searchprojectdemo.com/api/recommendations/similar/${product_id}/`);
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        widgetContainer.innerText = "Benzer ürün bulunamadı.";
        return;
      }

      widgetContainer.innerHTML = "<h3>Benzer Ürünler</h3>";

      data.forEach((item) => {
        const card = document.createElement("div");
        card.style.marginBottom = "10px";

        card.innerHTML = `
          <a href="${item.url}" target="_blank" style="text-decoration: none; color: inherit;">
            <img src="${item.image}" alt="${item.name}" width="100" />
            <p><strong>${item.name}</strong></p>
            <p>${item.price} TL</p>
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
