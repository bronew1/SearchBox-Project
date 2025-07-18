(function () {
  console.log("📦 Benzer ürün widget başlatıldı...");

  function extractSKUFromDOM() {
    const el = document.querySelector("p.product-info-sku");
    if (el?.textContent.includes("Ürün Kodu:")) {
      const sku = el.textContent.split("Ürün Kodu:")[1].trim();
      console.log("🛠️ SKU DOM’dan bulundu:", sku);
      return sku;
    }
    return null;
  }

  function renderWidget(sku) {
    if (!sku) {
      console.log("❌ SKU bulunamadı, widget durduruldu.");
      return;
    }

    const apiUrl = "https://searchprojectdemo.com/api/recommendations/similar/" + sku + "/";

    fetch(apiUrl)
      .then((res) => res.json())
      .then((data) => {
        const products = data.products || [];
        console.log("🧲 Benzer ürünler getirildi:", products);
        if (products.length === 0) return;

        const style = document.createElement("style");
        style.innerHTML = `
          #similar-products-slider {
            padding: 20px;
            margin-top: 40px;
            border-top: 1px solid #ccc;
            font-family: sans-serif;
          }
          #similar-products-slider h2 {
            font-size: 20px;
            margin-bottom: 12px;
          }
          .similar-products-grid {
            display: flex;
            overflow-x: auto;
            gap: 12px;
          }
          .similar-product-card {
            flex: 0 0 200px;
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 10px;
            background: #fff;
            text-align: center;
          }
          .similar-product-card img {
            max-width: 100%;
            height: auto;
          }
          .similar-product-card .price {
            font-weight: bold;
            margin-top: 4px;
          }
        `;
        document.head.appendChild(style);

        const container = document.createElement("div");
        container.id = "similar-products-slider";
        container.innerHTML = "<h2>Benzer Ürünler</h2>";

        const grid = document.createElement("div");
        grid.className = "similar-products-grid";

        products.forEach((p) => {
          const card = document.createElement("div");
          card.className = "similar-product-card";
          card.innerHTML = `
            <a href="${p.url}">
              <img src="${p.image}" alt="${p.name}" />
              <div>${p.name}</div>
              <div class="price">${p.price} TL</div>
            </a>`;
          grid.appendChild(card);
        });

        container.appendChild(grid);

        const targets = [
          ".product-detail",
          ".product-area",
          ".urun-detay",
          ".product-container",
          ".product-wrapper",
        ];
        let inserted = false;
        for (let i = 0; i < targets.length; i++) {
          const el = document.querySelector(targets[i]);
          if (el) {
            el.appendChild(container);
            inserted = true;
            break;
          }
        }

        if (!inserted) {
          document.body.appendChild(container);
        }
      })
      .catch((e) => console.error("❌ Benzer ürünler yüklenemedi:", e));
  }

  // 1️⃣ dataLayer.push override ile event yakalama
  const originalPush = window.dataLayer?.push;
  window.dataLayer = window.dataLayer || [];

  window.dataLayer.push = function () {
    const args = Array.from(arguments);
    for (const event of args) {
      if (event.event === "view_item" && event.product_id) {
        console.log("🎯 view_item yakalandı:", event);
        renderWidget(event.product_id);
      }
    }
    return originalPush.apply(window.dataLayer, arguments);
  };

  // 2️⃣ sayfa yüklendiğinde eski event varsa onu yakala
  setTimeout(() => {
    const initialEvent = window.dataLayer.find(
      (e) => e.event === "view_item" && e.product_id
    );
    if (initialEvent) {
      console.log("📦 view_item başlangıçta bulundu:", initialEvent);
      renderWidget(initialEvent.product_id);
    } else {
      // 3️⃣ fallback olarak DOM’dan dene
      const sku = extractSKUFromDOM();
      if (sku) renderWidget(sku);
    }
  }, 1000);
})();
