(function () {
  console.log("👀 Benzer ürün widget başlatıldı...");

  window.addEventListener("message", async (event) => {
    if (!event?.data || event.data.event_name !== "view_item") return;

    const { product_id } = event.data;
    if (!product_id) return;

    // Eğer daha önce eklenmişse tekrar ekleme
    if (document.querySelector("#similar-products-widget")) return;

    try {
      const res = await fetch(`https://searchprojectdemo.com/api/recommendations/similar/${product_id}/`);
      const data = await res.json();

      const verticalTab = document.querySelector(".vertical-tab");
      if (!verticalTab) return;

      const container = document.createElement("div");
      container.id = "similar-products-widget";
      container.innerHTML = `
        <h3 style="font-size: 20px; font-weight: 600; margin: 20px 0;">Benzer Ürünler</h3>
        <div class="similar-products-slider" style="display: flex; overflow-x: auto; gap: 16px;"></div>
      `;

      const slider = container.querySelector(".similar-products-slider");

      data.forEach(p => {
        const item = document.createElement("div");
        item.className = "product-best-wrapper";
        item.style.minWidth = "250px";
        item.innerHTML = `
          <div class="product-img">
            <a href="${p.url}">
              <img class="base-image" loading="lazy" width="250" height="250" src="${p.image}" alt="${p.name}" />
            </a>
            <a href="${p.url}">
              <img class="hover-image" loading="lazy" width="250" height="250" src="${p.image}" alt="${p.name}" />
            </a>
            <div class="hover-img-detail">
              <div class="product-code">${p.sku || ""}</div>
              <div>
                <a href="#" class="product-fav" data-sku="${p.sku || ""}">F</a>
                <a href="${p.url}" class="product-sepet">S</a>
              </div>
            </div>
          </div>
          <div class="product-ticket-wrapper"></div>
          <div class="product-detail">
            <a href="${p.url}" class="product-title stretched-link">${p.name}</a>
            <p class="product-discount"></p>
            <p class="price-wrapper">
              <span class="product-price">${p.price} TL</span>
            </p>
          </div>
        `;
        slider.appendChild(item);
      });

      verticalTab.parentNode.insertBefore(container, verticalTab.nextSibling);
    } catch (err) {
      console.error("❌ Widget verisi alınamadı:", err);
    }
  });
})();
