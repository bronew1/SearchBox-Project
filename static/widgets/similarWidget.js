(function () {
  console.log("👀 Benzer ürün widget başlatıldı...");

  // DOM'da widget div'i yoksa oluştur
  if (!document.querySelector("#similar-products-widget")) {
    const container = document.createElement("div");
    container.id = "similar-products-widget";
    container.style.position = "fixed";
    container.style.bottom = "20px";
    container.style.right = "20px";
    container.style.width = "300px";
    container.style.background = "#fff";
    container.style.border = "1px solid #ddd";
    container.style.padding = "10px";
    container.style.boxShadow = "0 2px 10px rgba(0,0,0,0.1)";
    container.style.zIndex = "9999";
    container.innerText = "⏳ Yükleniyor...";
    document.body.appendChild(container);
  }

  window.addEventListener("message", async (event) => {
    if (!event?.data || event.data.event_name !== "view_item") return;

    const { product_id } = event.data;

    if (!product_id) {
      console.error("❌ product_id bulunamadı, widget durduruldu.");
      return;
    }

    console.log("✅ Widget başlatılıyor, product_id:", product_id);

    const widgetContainer = document.querySelector("#similar-products-widget");
    widgetContainer.innerHTML = "⏳ Yükleniyor...";

    try {
      const response = await fetch(`https://searchprojectdemo.com/api/recommendations/similar/${product_id}/`);
      const data = await response.json();

      if (!Array.isArray(data) || data.length === 0) {
        widgetContainer.innerHTML = "<p>Benzer ürün bulunamadı.</p>";
        return;
      }

      widgetContainer.innerHTML = `<h3 style="margin-top:0; font-size:16px;">Benzer Ürünler</h3>`;

      data.forEach((item) => {
        const card = document.createElement("div");
        card.style.marginBottom = "10px";

        card.innerHTML = `
          <a href="${item.url}" target="_blank" style="text-decoration: none; color: inherit;">
            <img src="${item.image}" alt="${item.name}" width="100" style="border-radius: 4px;" />
            <p style="margin: 5px 0 0;"><strong>${item.name}</strong></p>
            <p style="margin: 0; color: #888;">${item.price} TL</p>
          </a>
        `;

        widgetContainer.appendChild(card);
      });

    } catch (err) {
      console.error("❌ Widget verisi alınamadı:", err);
      widgetContainer.innerHTML = "<p>Bir hata oluştu.</p>";
    }
  });
})();
