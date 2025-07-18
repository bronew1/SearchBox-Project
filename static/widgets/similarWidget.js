(function () {
  console.log("📦 Benzer ürün widget başlatıldı...");
  var checkCount = 0;
  var interval = setInterval(function () {
    checkCount++;
    if (checkCount > 30) clearInterval(interval); // 9 saniye deneme

    // view_item eventi dataLayer'da var mı kontrol et
    if (!window.dataLayer || !window.dataLayer.length) {
      console.log("❌ dataLayer henüz yok");
      return;
    }

    let sku = null;

    // 1️⃣ dataLayer'dan sku al
    const viewItemEvent = window.dataLayer.find(
      (e) => e.event === "view_item" && e.product_id
    );
    if (viewItemEvent) {
      sku = viewItemEvent.product_id;
      console.log("✅ SKU dataLayer’dan alındı:", sku);
    }

    // 2️⃣ Fallback: DOM'dan al
    if (!sku) {
      const skuText = document.querySelector("p.product-info-sku")?.textContent;
      if (skuText?.includes("Ürün Kodu:")) {
        sku = skuText.split("Ürün Kodu:")[1].trim();
        console.log("🛠️ SKU DOM’dan bulundu:", sku);
      }
    }

    if (!sku) {
      console.log("❌ SKU bulunamadı, widget durduruldu.");
      return;
    }

    clearInterval(interval);

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
            </a>
          `;
          grid.appendChild(card);
        });

        container.appendChild(grid);

        // Ekleme noktası
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
      .catch((e) => {
        console.error("❌ Benzer ürünler yüklenemedi:", e);
      });
  }, 300);
})();
